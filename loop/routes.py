from flask import render_template, url_for, flash, redirect, request
from loop import app, db, bcrypt
from loop.forms import RegistrationForm, LoginForm, GroupForm
from loop.models import Users
from flask_login import login_user, current_user, logout_user, login_required
from loop.cinema import CinemaMovies
from loop.additive_utilitarian import AdditiveUtilitarian

amount_of_people = 0


@app.route("/")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('home'))
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
    return render_template('profile.html', title='Profile')


@app.route("/group", methods=['GET', 'POST'])
@login_required
def group():
    global amount_of_people
    cinema = CinemaMovies()
    form = GroupForm()
    amount_of_people = form.amount.data
    return render_template('group.html', title='Group', form=form, number=form.amount.data,
                           cinema=cinema.get_list_of_movies())


@app.route("/group_recommendation", methods=['GET', 'POST'])
def get_group_recommendation():
    input_values = []
    if amount_of_people > 0:
        for index in range(0, amount_of_people*amount_of_people):
            input_values.append(int(request.form['myInput_' + str(index)]))

    additive = AdditiveUtilitarian()
    additive.get_values(input_values, amount_of_people)
    additive.get_user_ratings()
    return render_template('group_recommendation.html', title='Group recommendation', input_values=input_values)