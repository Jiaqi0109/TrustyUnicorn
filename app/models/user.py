from app.extensions import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    password = db.Column(db.String(16))
    email = db.Column(db.String(32))
    activate = db.Column(db.Boolean, default=0)
    pids = db.Column(db.Text)
    keywords = db.Column(db.Text)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
