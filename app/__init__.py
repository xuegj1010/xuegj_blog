from flask import Flask, redirect, url_for

from app.controllers import blog_blueprint
from app.controllers.blog import home
from .models import db
from .config import DevConfig


def create_app(object_name):
    app = Flask(__name__)

    app.config.from_object(DevConfig)

    db.init_app(app)

    # @app.route('/')
    # def index():
    #     return redirect(url_for(home))

    app.register_blueprint(blog_blueprint)

    return app
