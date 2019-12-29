from flask import render_template, url_for, flash, redirect, request
from loop import app, db, bcrypt
from loop.forms import RegistrationForm, LoginForm, GroupForm
from loop.models import Users
from flask_login import login_user, current_user, logout_user, login_required
from loop.cinema import CinemaMovies
from loop.algorithm import Algorithms
import re
import json
import urllib.request
import ssl

api_key = ""
base_url = "https://api.tmdb.org/3/discover/movie/?api_key="+api_key


@app.route("/")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/profile")
@login_required
def profile():
    ssl._create_default_https_context = ssl._create_unverified_context
    conn = urllib.request.urlopen(base_url)
    data = json.loads(conn.read())
    return render_template('profile.html', title='Profile', data=data)


@app.route("/group", methods=['GET', 'POST'])
@login_required
def group():
    cinema = CinemaMovies()
    form = GroupForm()
    return render_template('group.html', title='Group', form=form, group_size=form.amount.data,
                           cinema=cinema.get_cinema_movies())


@app.route("/group_recommendation", methods=['GET', 'POST'])
@login_required
def get_group_recommendation():
    cinema = CinemaMovies()
    input_values = []
    # Getting all the values from the group form
    for index in range(len(request.form)):
        try:
            input_values.append(request.form['myInput_' + str(index)])
        except KeyError:
            break

    # Checking if the form was completed
    if input_values:
        # Get the results from the algorithms
        algorithm = Algorithms(input_values)
        movies = algorithm.run()

        top_movie_details = []
        top_movie_image = []
        other_movie_details = []
        other_movie_images = []
        counter = 0
        for movie in movies:
            # Removing unwanted characters in the movie name
            movie_name_format = re.sub(r'[^\w\s]', '', movie["movie"])
            # replacing spaces with a "-"
            movie_name = movie_name_format.replace(' ', '-')
            cinema_link = cinema.get_movie_details()[1]
            movie_link = cinema_link + "movie/" + movie_name
            for title, movie_details in cinema.get_movie_details()[0].items():
                for movie_image, times in movie_details.items():
                    if title == movie["movie"]:
                        # Separating the most recommended movie and image
                        if counter == 0:
                            top_movie_details.append((title, times, movie["score"], movie_link))
                            top_movie_image.append(cinema_link+movie_image)
                        else:
                            other_movie_details.append((title, times, movie["score"], movie_link))
                            other_movie_images.append(cinema_link + movie_image)
            counter += 1
        return render_template('group_recommendation.html', title='Group recommendation', top_movie=top_movie_details,
                               top_movie_image=top_movie_image, movies=other_movie_details,
                               movie_images=other_movie_images)
    else:
        return redirect(url_for('group'))
