# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cache import Cache
from flask_login import LoginManager
from flask_openid import OpenID

db = SQLAlchemy()
mail = Mail()
cache = Cache()
login_manager = LoginManager()
oid = OpenID()
