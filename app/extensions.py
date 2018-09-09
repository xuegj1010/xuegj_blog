from flask import session
from flask_bcrypt import Bcrypt
from flask_oauthlib.client import OAuth
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_cache import Cache
from flask_assets import Environment, Bundle
from flask_admin import Admin

bcrypt = Bcrypt()
oauth = OAuth()
login_manager = LoginManager()
principals = Principal()
cache = Cache()
asset_env = Environment()
admin = Admin()

main_css = Bundle(
    'css/bootstrap.css',
    'css/bootstrap.min.css',
    'css/bootstrap-theme.css',
    filters='cssmin',
    output='assets/css/common.css'
)

main_js = Bundle(
    'js/bootstrap.js',
    'js/bootstrap.min.js',
    'js/jquery.min.js',
    filters='jsmin',
    output='assets/js/common.js'
)

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='1792074837557125',
    consumer_secret='50a6971936ceb060292f10cd7e7dffb8',
    request_token_params={'scope': 'email'})

login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.filter_by(id=user_id).first()


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_oauth_token')
