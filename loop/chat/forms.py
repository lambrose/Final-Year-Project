from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.widgets import html5
from wtforms.validators import DataRequired


# Create a socket group chat
class CreateRoom(FlaskForm):
    voters = IntegerField('Specify the amount of people entering the group that are voting:',
                          widget=html5.NumberInput(min=2, max=15), validators=[DataRequired()])
    submit = SubmitField('Create A Room')


# Enter into a preexisting group chat
class JoinRoom(FlaskForm):
    room = IntegerField('Specify the room number to enter:', widget=html5.NumberInput(min=1, max=100),
                        validators=[DataRequired()])
    submit = SubmitField('Join A Room')
