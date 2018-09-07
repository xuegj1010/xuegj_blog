from os import path
from uuid import uuid4

from flask import flash, url_for, redirect, render_template, request, session
from flask_login import login_user, logout_user

from app.controllers import main_blueprint
from app.extensions import facebook
from app.forms import LoginForm, RecaptchaField, RegisterForm
from app.models import db, User


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        flash('You have been logged in.', category='success')
        return redirect(url_for('blog.home'))
    return render_template('login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('blog.home'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(id=str(uuid4()), username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Your user has been created, please login.", category='success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main_blueprint.route('/facebook')
def facebook_login():
    return facebook.authorize(
        callback=url_for('main.facebook_authorized',
                         next=request.referrer or None,
                         _external=True)
    )


@main_blueprint.route('/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return f"Access denied: reason={request.args['error_reason']} error={request.args['error_description']}"

    session['facebook_oauth_token'] = (resp['access_token'], '')

    me = facebook.get('/me')

    if me.data.get('first_name', False):
        facebook_username = me.data['first_name'] + " " + me.data['last_name']
    else:
        facebook_username = me.data['name']

    user = User.query.filter_by(username=facebook_username).first()
    if user is None:
        user = User(id=str(uuid4()), username=facebook_username, password='jmilkfan')
        db.session.add(user)
        db.session.commit()

    flash('You have been logged in.', category='success')

    return redirect(url_for('blog.home'))
