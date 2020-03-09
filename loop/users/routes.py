from flask import render_template, url_for, flash, redirect, request, Blueprint
from loop import db, bcrypt
from loop.users.forms import RegistrationForm, LoginForm
from loop.models import Users
from flask_login import login_user, current_user, logout_user

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    # ensure that if the user is logged in, then they cannot register another account
    if current_user.is_authenticated:
        return redirect(url_for('main.watch'))
    form = RegistrationForm()
    # when the form has been filled and submitted, encypt the password before saving it in the database
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                     password=hashed_password)
        # adding this entry to the db
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/", methods=['GET', 'POST'])
@users.route("/login", methods=['GET', 'POST'])
def login():
    # ensure that if the user is logged in, then they cannot login to another account
    if current_user.is_authenticated:
        return redirect(url_for('main.watch'))
    form = LoginForm()
    # when the form has been filled and submitted, verify that the credentials are in the database
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # if there was a page clicked before the login, it will be redirected to it after the login
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.watch'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# logout function
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))
