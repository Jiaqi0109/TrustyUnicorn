from app.extensions import db


class Position(db.Model):

    __tablename__ = 'positions'

    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(32))
    city = db.Column(db.String(16))
    salary = db.Column(db.String(16))
    workyear = db.Column(db.String(16))
    education = db.Column(db.String(16))
    jobnature = db.Column(db.String(16))
    temptation = db.Column(db.Text)
    description = db.Column(db.Text)
    publish_time = db.Column(db.String(16))
    crawl_time = db.Column(db.DateTime)
