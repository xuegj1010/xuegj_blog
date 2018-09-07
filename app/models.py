from flask_login import AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_principal import current_app
from itsdangerous import Serializer, SignatureExpired, BadSignature

from .extensions import bcrypt, cache

db = SQLAlchemy()

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.String(45), db.ForeignKey('users.id')),
    db.Column('role_id', db.String(45), db.ForeignKey('roles.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    posts = db.relationship('Post', backref='users', lazy='dynamic')
    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

        default = Role.query.filter_by(name='default').one()
        self.roles.append(default)

    def __repr__(self):
        return f"<Model User `{self.username}`>"

    @staticmethod
    def set_password(password):
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    @staticmethod
    @cache.memoize(60)
    def verify_auth_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.filter_by(id=data['id']).first()
        return user


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Model Role `{self.name}`'


posts_tags = db.Table(
    'posts_tags',
    db.Column('post_id', db.String(45), db.ForeignKey('posts.id')),
    db.Column('tag_id', db.String(45), db.ForeignKey('tags.id'))
)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)

    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='posts', lazy='dynamic')
    tags = db.relationship('Tag', secondary=posts_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, id, title):
        self.title = title
        self.id = id

    def __repr__(self):
        return f"<Model Post `{self.title}`>"


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())

    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Model Comment `{self.name}`>'


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Model Tag `{self.name}`>"
