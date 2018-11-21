from instagram import db
from flask_login import UserMixin, current_user
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(30), unique=True, index=True)
    password = db.Column('password', db.Text)
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    avatar = db.Column('avatar', db.String(200))

    def __init__(self, username, email, password):
        self.username = username
        self.salting(password)
        self.email = email
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return f"<id.{self.id}> {self.username}"

    def salting(self,password):
        self.password = generate_password_hash(password)

    def salt_tasting(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

