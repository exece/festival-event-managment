#import flask - from the package import class
from flask import Flask, render_template 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db=SQLAlchemy()

# function creating a web application, web server will run the web app
def create_app():  
    app=Flask(__name__)  # package that is calling this app
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bootstrap = Bootstrap(app)

    app.debug=True
    app.secret_key='utroutoru'

    # set the app configuration data 
    # app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sitedata.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ['DATABASE_URL']
    
    # initialize db with flask app
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # error handling routes
    # invalid request handling
    @app.errorhandler(400)
    def page_not_found(e):
        error_code="400"
        error_message="Bad Request"
        return render_template('error.html', error_code=error_code, error_message=error_message), 400

    # page not found handling
    @app.errorhandler(404)
    def page_not_found(e):
        error_code="404"
        error_message="Page Not Found"
        return render_template('error.html', error_code=error_code, error_message=error_message), 404

    # server error handling
    @app.errorhandler(500)
    def internal_error(e):
        error_code="500"
        error_message="Internal Server Error"
        return render_template('error.html', error_code=error_code, error_message=error_message), 500

    # importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import events
    app.register_blueprint(events.bp)
    
    return app



