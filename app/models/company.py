from app.extensions import db


class Company(db.Model):

    __tablename__ = 'companies'

    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    full_name = db.Column(db.String(32))
    city = db.Column(db.String(16))
    logo = db.Column(db.String(128))
    industry = db.Column(db.String(32))
    finance_stage = db.Column(db.String(32))
    scale = db.Column(db.String(16))
    crawl_time = db.Column(db.DateTime)
