from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    plan = db.Column(db.String(45), nullable=False, default='free')

    def __init__(self, username, email, password, plan='free'):
        self.username = username
        self.email = email
        self.password = password
        self.plan = plan
