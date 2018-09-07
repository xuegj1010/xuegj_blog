from flask import Flask

from app.extensions import bcrypt, login_manager
from .controllers import blog_blueprint, main_blueprint
from .controllers.blog import home
from .models import db


def create_app(object_name):
    app = Flask(__name__)

    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)

    return app
