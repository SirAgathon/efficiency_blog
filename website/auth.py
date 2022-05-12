"""
Login, sign up, etc. functions
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash 

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for("views.home"))
            else:
                flash('Password is incorrect.', category = 'error')
        else:
            flash('Email does not exist.', category = 'error')

    return render_template("login.html", user=current_user)

@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_pass = request.form.get('password_')
        
        email_exists = User.query.filter_by(email = email).first()
        username_exists = User.query.filter_by(username = username).first()

        if email_exists:
            flash('Email exists!', category='error')
        elif username_exists:
            flash('Username already exists.', category = 'error')
        elif password != confirm_pass:
            flash('Passwords don\'t match', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category = 'error')
        elif len(password) < 6:
            flash('Password is too short!', category = 'error')
        # elif verify email
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash('User created!')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home")) # refers to home function in views.py; easier to change things in the future



