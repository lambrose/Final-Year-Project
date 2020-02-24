from loop import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    preference = db.relationship('Preferences', backref='author', lazy=True)
    group_result = db.relationship('GroupResults', backref='author', lazy=True)

    def __repr__(self):
        return f"Users('{self.id}', '{self.first_name}', '{self.last_name}', '{self.email}')"


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(100, collation='utf8_bin'), nullable=False)
    overview = db.Column(db.Unicode(2000, collation='utf8_bin'), nullable=False)
    image = db.Column(db.Unicode(100, collation='utf8_bin'), nullable=False)
    action = db.Column(db.Integer, nullable=True)
    adventure = db.Column(db.Integer, nullable=True)
    animation = db.Column(db.Integer, nullable=True)
    comedy = db.Column(db.Integer, nullable=True)
    crime = db.Column(db.Integer, nullable=True)
    documentary = db.Column(db.Integer, nullable=True)
    drama = db.Column(db.Integer, nullable=True)
    family = db.Column(db.Integer, nullable=True)
    fantasy = db.Column(db.Integer, nullable=True)
    history = db.Column(db.Integer, nullable=True)
    horror = db.Column(db.Integer, nullable=True)
    music = db.Column(db.Integer, nullable=True)
    mystery = db.Column(db.Integer, nullable=True)
    romance = db.Column(db.Integer, nullable=True)
    science_fiction = db.Column(db.Integer, nullable=True)
    tv_movie = db.Column(db.Integer, nullable=True)
    thriller = db.Column(db.Integer, nullable=True)
    war = db.Column(db.Integer, nullable=True)
    western = db.Column(db.Integer, nullable=True)
    popularity = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Movies('{self.id}', '{self.title}', '{self.overview}', '{self.popularity}', '{self.release_date}')"


class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.Unicode(100, collation='utf8_bin'), nullable=False)
    vote_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    like = db.Column(db.Integer, nullable=True)
    dislike = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Preference('{self.movie}', '{self.vote_date}', '{self.like}', '{self.dislike}')"


class GroupResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.Unicode(100, collation='utf8_bin'), nullable=False)
    additive = db.Column(db.Integer, nullable=True)
    multiplicative = db.Column(db.Integer, nullable=True)
    borda = db.Column(db.Integer, nullable=True)
    copeland = db.Column(db.Integer, nullable=True)
    plurality_voting = db.Column(db.Integer, nullable=True)
    approval = db.Column(db.Integer, nullable=True)
    least_misery = db.Column(db.Integer, nullable=True)
    most_pleasure = db.Column(db.Integer, nullable=True)
    average_without_misery = db.Column(db.Integer, nullable=True)
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"GroupResults('{self.id}', '{self.winner}', '{self.additive}', '{self.multiplicative}'," \
               f" '{self.borda}', '{self.copeland}', '{self.plurality_voting}', '{self.approval}'," \
               f" '{self.least_misery}', '{self.most_pleasure}', '{self.average_without_misery}', " \
               f"'{self.publish_date}')"
