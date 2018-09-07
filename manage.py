import os

from flask_assets import ManageAssets
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app, asset_env
from app.models import db, User, Post, Comment, Tag, Role

env = os.environ.get('BLOG_ENV', 'dev')
app = create_app(f'app.config.{env.capitalize()}Config')

manger = Manager(app)
migrate = Migrate(app, db)

manger.add_command('server', Server())
manger.add_command('db', MigrateCommand)
manger.add_command('assets', ManageAssets(asset_env))


@manger.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Post=Post,
        Comment=Comment,
        Tag=Tag,
        Server=Server,
        Role=Role
    )


if __name__ == '__main__':
    manger.run()
