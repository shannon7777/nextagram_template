import os
import boto3, botocore
from app import app
from flask_login import current_user
from models.user import User

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg', 'gif'])

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    user = User.get_by_id(current_user.id)
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            str(user.username) + "/" + file.filename,
            # file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    return f"{file.filename}"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
