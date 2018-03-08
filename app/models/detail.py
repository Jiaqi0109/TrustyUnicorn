from app.extensions import db


class Detail(db.Model):

    __tablename__ = 'details'

    pid = db.Column(db.Integer, primary_key=True)
    workyear = db.Column(db.String(16))
    education = db.Column(db.String(16))
    jobnature = db.Column(db.String(16))
    temptation = db.Column(db.Text)
    description = db.Column(db.Text)
    crawl_time = db.Column(db.DateTime)
