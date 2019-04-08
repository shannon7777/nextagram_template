from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from helpers.googleoauth import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__)

@sessions_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.get(User.username == username)

    if not user:
        flash("Username or password incorrect", "danger")
        next = request.args.get('next')
        return render_template('home.html')
    else:
        if check_password_hash(user.password, password):
            login_user(user)
            flash('You have logged in successfully!', 'success')
            return redirect(url_for('users.show', username=user.username))
        else:
            flash("username or password incorrect", "danger")
            return redirect(url_for('home'))

@sessions_blueprint.route('/login/google', methods=['GET'])
def google_login():
    redirect_uri = url_for('sessions.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google', methods=["GET"])
def authorize_google():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash("Logged in with Google successfully", "success")
        return redirect(url_for('users.show', username=current_user.username))
    else:
        flash("You don't seem to have an account yet. Please create one to continue.", "danger")
        return redirect(url_for('users.new'))


@sessions_blueprint.route('/delete')
def logout():
    logout_user()
    flash("logged out", "success")
    return redirect(url_for('home'))
