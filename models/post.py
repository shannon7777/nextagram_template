from app import app
import peewee as pw
from playhouse.hybrid import hybrid_property
from models.base_model import BaseModel
from models.user import User

class Post(BaseModel):
    user_id = pw.ForeignKeyField(User, backref='posts', unique=False, on_delete='CASCADE', index=True)
    caption = pw.TextField(null=True)
    image_path = pw.CharField(unique=True, null=True)

    @hybrid_property
    def image_url(self):
        user = User.get_by_id(self.user_id)
        if self.image_path:
            return app.config['S3_LOCATION'] + "/" + user.username + "/" + self.image_path


# https://s3-ap-southeast-1.amazonaws.com/ nextagram-clone-shannon/ shannonsimoncherry777/32_monkey1.jpeg_2019-04-03_194947.661251
# https://s3-ap-southeast-1.amazonaws.com/ nextagram-clone-shannon/ 32/32_monkey1.jpeg_2019-04-03_194947.661251