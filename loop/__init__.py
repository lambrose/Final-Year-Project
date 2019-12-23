from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dbb33057a46d3a750dec01c24dfabbc0'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://mydb3378al:jo6gal@mysql1.it.nuigalway.ie/mydb3378"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from loop import routes
