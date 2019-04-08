from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from models.post import Post
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers.helpers import upload_file_to_s3, allowed_file, app
import boto3, botocore
import datetime

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    re_password = request.form['re_password']
    
    user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

    if user.save() and password == re_password:
        flash('Successfully Created User', "success")
        login_user(user)
        return redirect(url_for('users.show'), username=username)
        # return redirect(url_for('new', first_name=first_name, last_name=last_name))
    else:
        flash('Failed to create user', "danger")
        return render_template('404.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    posts = Post.select()
    user = User.get_or_none(User.username==username)
    return render_template('userprofile.html', user=user, posts=posts)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(current_user.id)
    return render_template('editprofile.html', user=user)


@users_blueprint.route('/<username>/update', methods=['POST'])
def update(username):
    user = User.get_or_none(username=username)

    if current_user == user:
        if request.form['first_name']:
            user.first_name = request.form['first_name']
        if request.form['last_name']:
            user.last_name = request.form['last_name']
        if request.form['email']:
            user.email = request.form['email']
        if request.form['username']:
            user.username = request.form['username']

    if user.save():
        flash('Profile successfully updated', 'primary')
        return redirect(url_for('users.show', username=user.username))
    else: 
        flash('Error encounted, profile did not updated', 'danger')
        return redirect(url_for('users.edit', id=current_user.id))

@users_blueprint.route('/<id>/upload_profile', methods=['POST'])
def upload_profile(id):
    user = User.get_by_id(id)
    if request.files.get('user_file'):
        if "user_file" not in request.files:
            flash("No user_file key in request.files", "danger")

    file = request.files["user_file"]

    if file.filename == "":
        flash("Please select a file with a name", "danger")

    if file and allowed_file(file.filename):
        file.filename = secure_filename(str(id) + "_" + file.filename + "_"+ str(datetime.datetime.now())) # making the file name that takes id / filename / and the date-time it was posted 
        output = upload_file_to_s3(file, app.config["S3_BUCKET"]) # insert file into upload_file_to_s3 func as parameter and app.config with its aws bucket name
        user.profile_image_path = output # profile_image_path on DB is equals to output
        user.save()
        flash("Successfully uploaded profile image", "success")
        return redirect(url_for('users.show', username=current_user.username))
    else:
        flash("Only jpg, jpeg, png and gif files allowed.")
        return redirect(url_for('users.edit', id=current_user.id))

@users_blueprint.route('/<id>/toggle_privacy', methods=['POST'])
def toggle_privacy(id):
    user = User.get_by_id(id)
    # user = User.get(User.id == current_user.id)
    if current_user == user:
        user.update(is_private = not user.is_private).where(User.id == current_user.id).execute()
        flash('Succesfully updated profile privacy settings', "info")
        return redirect(url_for('users.show', username = current_user.username)) 
    else:
        flash('You are not authorized to do that','danger')
        return redirect(url_for('home'))
    
         