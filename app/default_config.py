import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
ADMINS = frozenset(['your@email.here'])
SECRET_KEY = 'YOURSECRETKEYHERE'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'somesecretkeyhere'

BOOTSTRAP_SERVE_LOCAL = True

CACHE_TYPE = 'simple'
