from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectMultipleField, widgets
from wtforms import SelectField, HiddenField
from wtforms.widgets import html5
from wtforms.validators import DataRequired, Length


# Group feature form
class GroupForm(FlaskForm):
    amount = IntegerField('How many people are in the group?', widget=html5.NumberInput(min=2, max=10),
                          validators=[DataRequired()])
    submit = SubmitField('Submit')


# Creating a check form for the cinema movies
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def cinema_list(cinema_movies):
    class CinemaForm(FlaskForm):
        pass

    # create a list of value/description tuples
    movie_choices = [(movie, movie) for movie in cinema_movies]
    options = MultiCheckboxField('Label', choices=movie_choices)
    # calling a javascript function button when clicked
    submit = SubmitField("Confirm", render_kw={"onclick": "movies_selected()"})
    send = SubmitField("Confirm")
    setattr(CinemaForm, "options", options)
    setattr(CinemaForm, "submit", submit)
    setattr(CinemaForm, "send", send)
    return CinemaForm()


# watch feature, search bar
class MovieSearchForm(FlaskForm):
    search = StringField('Movie:', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Search')


# Dropdown for movie genres
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


# specify if you like or dislike the movie
class LikeForm(FlaskForm):
    like_movie = HiddenField('Like:')
    submit = SubmitField('Like')


class DislikeForm(FlaskForm):
    dislike_movie = HiddenField('Dislike:')
    submit = SubmitField('Dislike')


class DeleteAllForm(FlaskForm):
    delete_records = HiddenField('Remove All:')
    submit = SubmitField('Delete All')
