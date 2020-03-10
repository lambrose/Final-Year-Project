import re
from flask import render_template, url_for, flash, redirect, request, Blueprint
from loop import db
from loop.collaborative_filter import CollaborativeFilter
from loop.main.forms import GroupForm, cinema_list, MovieSearchForm, SelectGenreForm, ContactForm
from loop.main.forms import LikeForm, DislikeForm, DeleteAllForm
from loop.group_history import GroupHistory
from loop.models import Movies, Preferences, GroupResults
from flask_login import current_user, login_required
from loop.cinema import CinemaMovies
from loop.algorithm import Algorithms
from loop.movie_search import MovieSearch
from loop.movie_categories import Genres
import unidecode
from loop import mail
from flask_mail import Message

# from loop.update_movie_db import UpdateMovieDatabase

main = Blueprint('main', __name__)


@main.route("/watch", methods=['GET', 'POST'])
@login_required
def watch():
    # update_db = UpdateMovieDatabase()
    # update_db.insert_movies()
    # initialise forms
    form = MovieSearchForm()
    like_form = LikeForm()
    dislike_form = DislikeForm()
    # check if the form has been submitted
    if like_form.is_submitted() and like_form.like_movie.data:
        # Query the database to get the selected movie
        preference = Preferences.query.filter_by(movie=like_form.like_movie.data, user_id=current_user.id).first()
        # if the movie is not found in the db, then add it
        if not preference:
            liked_movie = Preferences(movie=like_form.like_movie.data, author=current_user, like=1, dislike=0)
            db.session.add(liked_movie)
            db.session.commit()
            flash('You liked ' + like_form.like_movie.data, 'success')
        # if the movie is found and has the same preference, then remove it
        elif preference.like == 1:
            delete_vote(preference.id)
        # else change the preference type
        else:
            update_vote(preference.id)

    if dislike_form.is_submitted() and dislike_form.dislike_movie.data:
        preference = Preferences.query.filter_by(movie=dislike_form.dislike_movie.data, user_id=current_user.id).first()
        if not preference:
            disliked_movie = Preferences(movie=dislike_form.dislike_movie.data, author=current_user, like=0, dislike=1)
            db.session.add(disliked_movie)
            db.session.commit()
            flash('You disliked ' + dislike_form.dislike_movie.data, 'success')
        elif preference.like == 0:
            delete_vote(preference.id)
        else:
            update_vote(preference.id)

    # get all the voted on movie for the current user
    already_voted = Preferences.query.filter_by(user_id=current_user.id)
    movie_choices = {movie.movie: (movie.like, movie.dislike) for movie in already_voted}

    # initialise the collaborative filter
    collaborative_filter = CollaborativeFilter()
    genre_form = SelectGenreForm()
    genres = Genres()
    # global selected_genre
    selected_genre = {}
    if genre_form.genre.data not in ['None', 'Select']:
        selected_genre = genres.movies_genres(genre_form.genre.data)
    return render_template('watch.html', title='Watch', form=form, genre_form=genre_form, like_form=like_form,
                           already_voted=movie_choices, dislike_form=dislike_form, selected_genre=selected_genre,
                           popular_latest_movies=genres.popular_latest_movies(),
                           collaborative_filter=collaborative_filter.get_recommendation())


@main.route("/movie_recommendation", methods=['GET', 'POST'])
@login_required
def movie_recommendation():
    # when the form is submitted, this method gets the value of the form request
    movie = request.form.get("search")
    if movie:
        # search for the movie or a bit of of the movie in the db
        search_result = Movies.query.filter(Movies.title.ilike('%' + movie + '%')).first()
        if search_result:
            # get the recommendation from movies passed in
            movies = MovieSearch(search_result)
            return render_template('movie_recommendation.html', title='Movie recommendation',
                                   movies=movies.get_recommendation())
        # if the movie passed in is not in the db
        else:
            flash('Search Unsuccessful. Please check spelling again.', 'danger')
    return redirect(url_for('main.watch'))


@main.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    # deleting all values in a particular section
    delete_all_form = DeleteAllForm()
    if delete_all_form.is_submitted():
        # delete all liked movies
        if delete_all_form.delete_records.raw_data[1] == "like":
            likes = Preferences.query.filter_by(like=1, user_id=current_user.id)
            for like in likes:
                delete_vote(like.id)
        elif delete_all_form.delete_records.raw_data[1] == "dislike":
            # delete all disliked movies
            dislikes = Preferences.query.filter_by(dislike=1, user_id=current_user.id)
            for dislike in dislikes:
                delete_vote(dislike.id)
        else:
            # delete all group recommendations
            records = GroupResults.query.filter_by(user_id=current_user.id)
            for record in records:
                delete_group_vote(record.id)

    # get voted on movies
    likes = Preferences.query.filter_by(like=1, user_id=current_user.id)
    dislikes = Preferences.query.filter_by(dislike=1, user_id=current_user.id)
    # declare the group history data
    group_history = GroupHistory()
    history = group_history.get_history()
    # group history list of data for the graph
    ranking = group_history.get_rankings()
    return render_template('profile.html', likes=likes, dislikes=dislikes, history=history, group_values=ranking,
                           delete_all_form=delete_all_form)


@main.route("/profile/<int:vote_id>/update", methods=['GET', 'POST'])
@login_required
def update_vote(vote_id):
    # swap the values from a like to dislike or vice versa for movies already rated
    movie = Preferences.query.get_or_404(vote_id)
    if movie.like == 1:
        movie.like = 0
        movie.dislike = 1
        flash(movie.movie + ' has been added to your disliked list', 'success')
    else:
        movie.like = 1
        movie.dislike = 0
        flash(movie.movie + ' has been added to your liked list', 'success')
    db.session.commit()
    return redirect(url_for('main.profile'))


@main.route("/profile/<int:vote_id>/delete", methods=['POST'])
@login_required
def delete_vote(vote_id):
    # remove the previous voted preference for a particular movie
    movie = Preferences.query.get_or_404(vote_id)
    db.session.delete(movie)
    db.session.commit()
    if movie.like == 1:
        flash(movie.movie + ' has been removed from your liked list', 'success')
    else:
        flash(movie.movie + ' has been removed from your disliked list', 'success')
    return redirect(url_for('main.profile'))


@main.route("/profile/<int:group_id>/delete_record", methods=['POST'])
@login_required
def delete_group_vote(group_id):
    # remove the previous group history record
    group_result = GroupResults.query.get_or_404(group_id)
    db.session.delete(group_result)
    db.session.commit()
    flash(group_result.winner + ' has been removed', 'success')
    return redirect(url_for('main.profile'))


@main.route("/group_landing", methods=['GET', 'POST'])
@login_required
def group_landing():
    # render a landing page, for a user to specify the group options
    return render_template('group_landing.html', title='Group Landing')


@main.route("/group", methods=['GET', 'POST'])
@login_required
def group():
    # get the cinema form check list with all the current movie sin the cinema
    cinema_movies = CinemaMovies()
    people_form = GroupForm()
    cinema_form = cinema_list(cinema_movies.get_movies())
    return render_template('group.html', title='Group', people_form=people_form, group_size=people_form.amount.data,
                           cinema_form=cinema_form)


# This is used for the access the eye cinema movie website
def format_movie_title(movie):
    # Removing unwanted characters in the movie name except for a hyphen '-'
    format_title = re.sub(r'[^\w\s-]', '', movie["movie"])
    unaccented_string = unidecode.unidecode(format_title)
    # replacing spaces with a "-"
    return unaccented_string.replace(' ', '-')


@main.route("/group_recommendation", methods=['GET', 'POST'])
@login_required
def get_group_recommendation():
    cinema_movies = CinemaMovies()
    cinema_details = cinema_movies.get_movie_details()
    group_ratings_form = []
    # Getting all the values from the group form
    for index in range(len(request.form)):
        try:
            group_ratings_form.append(request.form['input_rating_' + str(index)])
        except KeyError:
            break

    # Checking if the form was completed
    if group_ratings_form:
        # Get the results from the algorithms
        algorithm = Algorithms(group_ratings_form)
        movies = algorithm.run()
        top_movie, other_movies = [], []
        counter = 0
        for movie in movies:
            cinema_url = cinema_details[1]
            movie_url = cinema_url + "movie/" + format_movie_title(movie)
            for title, movie_details in cinema_details[0].items():
                if title == movie["movie"]:
                    for image, times in movie_details.items():
                        # Separating the most recommended movie and image
                        if counter == 0:
                            top_movie = [title, cinema_url + image, times, movie["score"], movie_url]
                        else:
                            other_movies.append((title, cinema_url + image, times, movie["score"], movie_url))
            counter += 1
        return render_template('group_recommendation.html', title='Group recommendation', top_movie=top_movie,
                               other_movies=other_movies)
    else:
        return redirect(url_for('main.group'))


@main.route("/contact", methods=['POST', 'GET'])
def contact():
    # initialise form
    contact_form = ContactForm()
    # if form is completed, then end email
    if contact_form.validate_on_submit():
        send_email(request.form)
        # redirect to watch page
        return redirect(url_for('main.watch'))

    return render_template('contact.html', form=contact_form)


def send_email(message):
    # send email to loop and sender email
    email = Message(message.get('subject'), sender=message.get('email'), recipients=['loopfyp@gmail.com',
                    message.get('email')], body=message.get('message'))
    mail.send(email)
