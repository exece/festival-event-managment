from flask import (Blueprint, flash, render_template, request, url_for, redirect) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db

#create a blueprint
bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    # if the form is validated
    if (register.validate_on_submit() == True):
            # get username, password and email from form
            uname = register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            # check if that user exists already
            u1 = User.query.filter_by(name=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            # create password hash
            pwd_hash = generate_password_hash(pwd)
            # user object creation
            new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
            # db commit
            db.session.add(new_user)
            db.session.commit()
            # redirect to main page
            return redirect(url_for('main.index'))
    # the else is called when there is a get message
    else:
        return render_template('user.html', form=register, heading='Register')

# Login handling
@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        # get the username and password from the database
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        # if there is no user with that name
        if u1 is None:
            error='Incorrect user name'
        # check pwd
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            # set login_user of flask_login to manage user
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            # flash an error on the html page if anything
            flash(error) 
    return render_template('user.html', form=login_form, heading='Login')

# Logout handling
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

