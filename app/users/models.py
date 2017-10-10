from ..extensions import db
from werkzeug import generate_password_hash, check_password_hash
from app.users import constants as USER
from flask_login import UserMixin
from ..utils import get_current_time

class User(db.Model, UserMixin):
    __tablename__ = 'ethers_user'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    openid = db.Column(db.String(120), unique=True)
    activation_key = db.Column(db.String(120))
    created_time = db.Column(db.DateTime, default=get_current_time)

    _password = db.Column('password', db.String(120), nullable=False)
    
    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        if self.password is None:
            return False

        return check_password_hash(self.password, password)

    role_code = db.Column(db.SmallInteger, default=USER.USER, nullable=False)

    @property
    def role(self):
        return USER.USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == USER.ADMIN

    status_code = db.Column(db.SmallInteger, default=USER.NEW)
    
    @property
    def status(self):
        return USER.USER_STATUS[self.status_code]

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.nickname == login, User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first_or_404()
