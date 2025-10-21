from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_App():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gsgsgggdsfsdsd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    
    # --- LOGIN MANAGER ---
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'   # name of your login route
    login_manager.init_app(app)

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .model import User,Note

    create_database(app)


    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.drop_all()
            db.create_all()
        print('Create Database')

