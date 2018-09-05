from main import app
from models import db, User, Post, Comment, Tag

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

manger = Manager(app)
migrate = Migrate(app, db)
manger.add_command('server', Server())
manger.add_command('db', MigrateCommand)


@manger.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Post=Post,
        Comment=Comment,
        Tag=Tag
    )


if __name__ == '__main__':
    manger.run()
