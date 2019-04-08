from app import app
import peewee as pw
from playhouse.hybrid import hybrid_property
from models.base_model import BaseModel
from models.user import User
from models.post import Post

class Donations(BaseModel):
    user_id = pw.ForeignKeyField(User, backref='donations', unique=False, on_delete='CASCADE', index=True)
    amount = pw.DecimalField(decimal_places=2)
    post_id = pw.ForeignKeyField(Post, backref='donations', on_delete='CASCADE')
