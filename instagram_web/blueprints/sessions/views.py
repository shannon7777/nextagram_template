from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

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


@sessions_blueprint.route('/delete')
def logout():
    logout_user()
    flash("logged out", "success")
    return redirect(url_for('home'))
