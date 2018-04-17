from app.extensions import db


class User(db.Model):

    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    password = db.Column(db.String(16))
    email = db.Column(db.String(32))
    activate = db.Column(db.Boolean, default=0)
    pids = db.Column(db.Text)
    keywords = db.Column(db.Text)
