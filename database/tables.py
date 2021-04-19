from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tinhte(db.Model):
    __tablename__ = "tinhte"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)

    comments = db.relationship("TinhteComment", backref="id", lazy=True)


class TinhteComment(db.Model):
    __tablename__ = "tinhte_comment"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)

    tinhte_id = db.Column(db.Integer, db.ForeignKey("tinhte.id"))