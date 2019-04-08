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
    is_private = pw.BooleanField(default=False)

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

    @hybrid_property
    # Users list of people I'M FOLLOWING
    def list_of_idols_ids(self):
        return [idol.idol_id for idol in self.idols if idol.is_approved]

    @hybrid_property
    # Users list of people FOLLOWING YOU
    def list_of_fans_ids(self):
        return [fan.fan_id for fan in self.fans if fan.is_approved]  


