from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from app.extensions import bcrypt, login_manager, principals, cache, asset_env, main_css, main_js
from .controllers import blog_blueprint, main_blueprint
from .controllers.blog import home
from .models import db


def create_app(object_name):
    app = Flask(__name__)

    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    cache.init_app(app)
    asset_env.init_app(app)
    asset_env.register('main_js', main_js)
    asset_env.register('main_css', main_css)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)

    return app
