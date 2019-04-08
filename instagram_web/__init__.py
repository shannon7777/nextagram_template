from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from instagram_web.blueprints.payments.views import payments_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from helpers.googleoauth import oauth
import os
# from helpers.googleoauth import oauth
# import config



assets = Environment(app)
assets.register(bundles)

csrf = CSRFProtect(app)

oauth.init_app(app)

# BRAINTREE


# gateway = braintree.BraintreeGateway(
#     braintree.Configuration(
#         environment=os.environ.get('BT_ENVIRONMENT'),
#         merchant_id=os.environ.get('BT_MERCHANT_ID'),
#         public_key=os.environ.get('BT_PUBLIC_KEY'),
#         private_key=os.environ.get('BT_PRIVATE_KEY')
#     )
# )


# app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(payments_blueprint, url_prefix="/payments")

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return User.get_or_none(id=id)

login_manager.login_view = "users.show"
login_manager.login_message = u'Successfully logged in!'
login_manager.login_message_category = 'success'

@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    return render_template('home.html')