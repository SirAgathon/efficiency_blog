from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

"""
Enables website folder to become a python package
"""

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__) # First thing you need to do when creating a Flask app; __name__ references module we're going to be running to create this app
    app.config['SECRET_KEY'] = "siragathon" # in production this should be private and encrypted
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Indicate where database is and initiate app 
    db.init_app(app)

    from .views import views # relative imports
    from .auth import auth

    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # If user is not logged in, redirect to login page
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app): # Check if database exists, create if not
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")


