import os
import sys

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_login import login_user, current_user
from markupsafe import escape

from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from app.utils import user_is_authenticated
from .extensions import db, mail, cache, login_manager, oid
from app.users.models import User
from app.users.views import users as usersModule
from app.nav import nav, ExtendedNavbar, init_custom_nav_renderer

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)

    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    
    login_manager.login_view = 'users.login'
    login_manager.refresh_view = 'users.login'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    login_manager.init_app(app)
    Bootstrap(app)

    oid.init_app(app)

    app.register_blueprint(usersModule)
    nav.init_app(app)
    init_custom_nav_renderer(app)

    return app

def install_secret_key(app, filename='secret_key'):
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No Secret Key! Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)

app = create_app()

if not app.config['DEBUG']:
    install_secret_key(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index/index.html');

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

nav.register_element('frontend_top', ExtendedNavbar(
    title=View('Home', '.index'),
    root_class='navbar navbar-default',
    right_items=(
        Text('Moop'),
        View('Register', 'users.register')
    )
))
