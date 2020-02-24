import re
from flask import render_template, url_for, flash, redirect, request
from loop import app, db, bcrypt
from loop.collaborative_filter import CollaborativeFilter
from loop.forms import RegistrationForm, LoginForm, GroupForm, cinema_list, MovieSearchForm, SelectGenreForm
from loop.forms import LikeForm, DislikeForm
from loop.group_history import GroupHistory
from loop.models import Users, Movies, Preferences
from flask_login import login_user, current_user, logout_user, login_required
from loop.cinema import CinemaMovies
from loop.algorithm import Algorithms
from loop.movie_search import MovieSearch
from loop.movie_categories import Genres
import unidecode

# selected_genre = {}


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('watch'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                     password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('watch'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('watch'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/watch", methods=['GET', 'POST'])
@login_required
def watch():
    form = MovieSearchForm()
    like_form = LikeForm()
    dislike_form = DislikeForm()
    if like_form.is_submitted() and like_form.like_movie.data:
        preference = Preferences.query.filter_by(movie=like_form.like_movie.data, user_id=current_user.id).first()
        if not preference:
            liked_movie = Preferences(movie=like_form.like_movie.data, author=current_user, like=1, dislike=0)
            db.session.add(liked_movie)
            db.session.commit()
            flash('You liked ' + like_form.like_movie.data, 'success')
        elif preference.like == 1:
            delete_vote(preference.id)
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

    already_voted = Preferences.query.filter_by(user_id=current_user.id)
    movie_choices = {movie.movie: (movie.like, movie.dislike) for movie in already_voted}

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


@app.route("/movie_recommendation", methods=['GET', 'POST'])
@login_required
def movie_recommendation():
    movie = request.form.get("search")
    if movie:
        search_result = Movies.query.filter(Movies.title.ilike('%'+movie+'%')).first()
        if search_result:
            movies = MovieSearch(search_result)
            return render_template('movie_recommendation.html', title='Movie recommendation',
                                   movies=movies.get_recommendation())
        else:
            flash('Search Unsuccessful. Please check spelling again.', 'danger')
    return redirect(url_for('watch'))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    likes = Preferences.query.filter_by(like=1, user_id=current_user.id)
    dislikes = Preferences.query.filter_by(dislike=1, user_id=current_user.id)
    group_history = GroupHistory()
    history = group_history.get_history()
    ranking = group_history.get_rankings()
    return render_template('profile.html', likes=likes, dislikes=dislikes, history=history, group_values=ranking)


@app.route("/profile/<int:vote_id>/update", methods=['GET', 'POST'])
@login_required
def update_vote(vote_id):
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
    return redirect(url_for('profile'))


@app.route("/profile/<int:vote_id>/delete", methods=['POST'])
@login_required
def delete_vote(vote_id):
    movie = Preferences.query.get_or_404(vote_id)
    db.session.delete(movie)
    db.session.commit()
    if movie.like == 1:
        flash(movie.movie + ' has been removed from your liked list', 'success')
    else:
        flash(movie.movie + ' has been removed from your disliked list', 'success')
    return redirect(url_for('profile'))


@app.route("/group", methods=['GET', 'POST'])
@login_required
def group():
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


@app.route("/group_recommendation", methods=['GET', 'POST'])
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
        return redirect(url_for('group'))
