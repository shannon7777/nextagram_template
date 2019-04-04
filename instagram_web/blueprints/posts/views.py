from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from models.post import Post
from models.user import User
from werkzeug.utils import secure_filename
from helpers.helpers import upload_file_to_s3, allowed_file, app
from flask_login import current_user
import boto3, botocore
import datetime

posts_blueprint = Blueprint('posts',
                            __name__,
                            template_folder='templates')



@posts_blueprint.route('/upload', methods=['POST'])
def create():
    caption = request.form.get('caption')
    user_id = current_user.id

    if request.files.get('user_file'):
        if "user_file" not in request.files:
            flash("No user_file key in request.files", "danger")

    file = request.files["user_file"]

    if file.filename == "":
        flash("Please select a file with a name", "danger")

    if file and allowed_file(file.filename):
        file.filename = secure_filename(str(user_id) + "_" + file.filename + "_" + str(datetime.datetime.now()))
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        if Post.create(user_id=user_id, caption=caption, image_path=output):
            flash("Successfully uploaded user image", "success")
            return redirect(url_for('users.show', username=current_user.username))
    else:
        flash("Only jpg, jpeg, png and gif files allowed.", 'danger')
        return redirect(url_for('posts.edit', id=current_user.id))

