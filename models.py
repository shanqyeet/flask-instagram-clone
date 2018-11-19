from database import db
from flask_login import UserMixin
from database import login

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<id.{self.id}> {self.username}"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
