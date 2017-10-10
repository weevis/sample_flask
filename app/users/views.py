from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user
from ..extensions import db
from app.users.forms import RegisterForm, LoginForm
from app.users.models import User
from app.users.decorators import requires_login

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/me/')
@requires_login
def home():
    return render_template("users/profile.html", user=g.user)

@users.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@users.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.nickname.data, form.password.data)

        if user and authenticated:
            if login_user(user):
                session['user_id'] = user.id
                flash('Welcome %s' % user.name)
                return redirect(url_for('users.home'))

    flash('Wrong name or password', 'error-message')
    return render_template("users/login.html", form=form)

@users.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registration Form
    """
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # create an user instance not yet stored in the database
        user = User(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        # Log the user in, as he now has an id
        session['user_id'] = user.id

        # flash will display a message to the user
        flash('Thanks for registering')
        # redirect user to the 'home' method of the user module.
        return redirect(url_for('users.home'))

    return render_template("users/register.html", form=form)

@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('app.index')) 
