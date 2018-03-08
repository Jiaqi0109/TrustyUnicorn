from app.extensions import db


class Position(db.Model):

    __tablename__ = 'positions'

    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(32))
    salary = db.Column(db.String(16))
    city = db.Column(db.String(16))
    publish_time = db.Column(db.String(16))
    c_name = db.Column(db.String(16))
    c_full_name = db.Column(db.String(32))
    crawl_time = db.Column(db.DateTime)
