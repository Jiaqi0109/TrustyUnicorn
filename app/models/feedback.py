from app.extensions import db


class Feedback(db.Model):

    __tablename__ = 'feedback'

    fid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    deal = db.Column(db.Boolean, default=0)
