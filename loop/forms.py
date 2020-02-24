from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectMultipleField, widgets
from wtforms import SelectField, HiddenField
from wtforms.widgets import html5
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from loop.models import Users


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class GroupForm(FlaskForm):
    amount = IntegerField('How many people are in the group?', widget=html5.NumberInput(min=2, max=10),
                          validators=[DataRequired()])
    submit = SubmitField('Submit')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def cinema_list(cinema_movies):
    class CinemaForm(FlaskForm):
        pass

    # create a list of value/description tuples
    movie_choices = [(movie, movie) for movie in cinema_movies]
    options = MultiCheckboxField('Label', choices=movie_choices)
    submit = SubmitField("Confirm", render_kw={"onclick": "movies_selected()"})
    setattr(CinemaForm, "options", options)
    setattr(CinemaForm, "submit", submit)
    return CinemaForm()


class MovieSearchForm(FlaskForm):
    search = StringField('Movie:', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Search')


class SelectGenreForm(FlaskForm):
    genre = SelectField('Select Genre:',
                        choices=[('Select', 'Select'), ('Action', 'Action'), ('Adventure', 'Adventure'),
                                 ('Animation', 'Animation'), ('Comedy', 'Comedy'), ('Crime', 'Crime'),
                                 ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'),
                                 ('Fantasy', 'Fantasy'), ('History', 'History'), ('Horror', 'Horror'),
                                 ('Music', 'Music'), ('Mystery', 'Mystery'), ('Romance', 'Romance'),
                                 ('Science Fiction', 'Science Fiction'), ('Thriller', 'Thriller'),
                                 ('TV Movie', 'TV Movie'), ('War', 'War'), ('Western', 'Western')])
    submit = SubmitField('Confirm')


class LikeForm(FlaskForm):
    like_movie = HiddenField('Like:')
    submit = SubmitField('Like')


class DislikeForm(FlaskForm):
    dislike_movie = HiddenField('Dislike:')
    submit = SubmitField('Dislike')
