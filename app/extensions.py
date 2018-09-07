from flask import session
from flask_bcrypt import Bcrypt
from flask_oauthlib.client import OAuth

bcrypt = Bcrypt()
oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='1792074837557125',
    consumer_secret='50a6971936ceb060292f10cd7e7dffb8',
    request_token_params={'scope': 'email'})


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_oauth_token')
