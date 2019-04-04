from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw
from playhouse.hybrid import hybrid_property
from app import app

class User(UserMixin, BaseModel):
    first_name = pw.CharField(unique=False, null=False)
    last_name = pw.CharField(unique=False,null = False)
    email = pw.CharField(unique=True, index=True)
    username = pw.CharField(unique=True, index=True)
    password = pw.CharField(index=True)
    profile_image_path = pw.CharField(null=True)

    def validate(self):
        if len(self.password) < 6:
            self.errors.append("Password must be at least 6 characters!")
        if len(self.username) < 5:
            self.errors.append('Username must be at least 5 characteers long!')
        # if self.email 
        if not self.password:
            self.errors.append('You must enter a password!')

    @hybrid_property
    def profile_image_url(self):
        if self.profile_image_path:
            return app.config['S3_LOCATION'] + "/" + self.username + "/" + self.profile_image_path
        else:
            return app.config['S3_LOCATION'] + '40_profile-placeholder.png_2019-04-03_122504.525938'

        


