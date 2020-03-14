from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from loop.config import Config
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_sslify import SSLify


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
socketio = SocketIO()
mail = Mail()
sslify = SSLify()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from loop.users.routes import users
    from loop.main.routes import main
    from loop.chat.routes import chat

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)
    sslify.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(chat)
    return app
