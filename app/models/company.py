from app.extensions import db


class Company(db.Model):

    __tablename__ = 'companies'

    cid = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(128))
    industry = db.Column(db.String(32))
    scale = db.Column(db.String(16))
    finance_stage = db.Column(db.String(32))
