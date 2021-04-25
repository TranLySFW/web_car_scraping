from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# C:\Program Files\PostgreSQL\13\bin>pg_dump.exe -d muse_media --username=postgres  > muse_media.sql
# C:\Program Files\PostgreSQL\13\bin>psql.exe --username=postgres -d test < muse_media.sql

class Tinhte_Article(db.Model):
    __tablename__ = "tinhte_article"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    subject = db.Column(db.String)
    date = db.Column(db.Date)
    title = db.Column(db.String)
    content = db.Column(db.Text)

    tags = db.relationship("Tinhte_Tag", backref="article_id", lazy=True)
    comments = db.relationship("Tinhte_Comment", backref="article_id", lazy=True)


class Tinhte_Comment(db.Model):
    __tablename__ = "tinhte_comment"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    tinhte_article_id = db.Column(db.Integer, db.ForeignKey("tinhte_article.id"))


class Tinhte_Tag(db.Model):
    __tablename__ = "tinhte_tag"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)

    tinhte_article_id = db.Column(db.Integer, db.ForeignKey("tinhte_article.id"))
