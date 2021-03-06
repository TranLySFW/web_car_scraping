from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# C:\Program Files\PostgreSQL\13\bin>pg_dump.exe -d muse_media --username=postgres  > muse_media.sql
# C:\Program Files\PostgreSQL\13\bin>psql.exe --username=postgres -d test < muse_media.sql
# C:\Program Files\PostgreSQL\13\bin>pg_dump.exe -h 34.87.145.78 -p 3306 --username=tranly --password=mariana -t tinhte_article muse >  update_tinhte.sql
# C:\Program Files\PostgreSQL\13\bin>psql -h localhost -p 5432 --username=postgres --password=zxcvbnm1 -d muse_media -f update_tinhte.sql
# C:\Program Files\PostgreSQL\13\bin>pg_dump.exe -h localhost -p 5432 --username=postgres --password=zxcvbnm1 -t cafef_bank -d muse_media > update_cafef_bank.sql
# C:\Program Files\PostgreSQL\13\bin>psql -h 34.87.145.78 -p 3306 --username=tranly --password=mariana -d muse -f update_cafef_bank.sql


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
    tokenized_text = db.Column(db.String)
    prediction = db.Column(db.String)

    tinhte_article_id = db.Column(db.Integer, db.ForeignKey("tinhte_article.id"))


class Tinhte_Tag(db.Model):
    __tablename__ = "tinhte_tag"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)

    tinhte_article_id = db.Column(db.Integer, db.ForeignKey("tinhte_article.id"))


class Otofun_MainNode(db.Model):
    __tablename__ = "otofun_main_node"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    subject = db.Column(db.String)

    threads = db.relationship("Otofun_Thread", backref="node_id", lazy=True)


class Otofun_Thread(db.Model):
    __tablename__ = "otofun_thread"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    subject = db.Column(db.String)
    last_update = db.Column(db.Date)

    main_node_id = db.Column(db.Integer, db.ForeignKey("otofun_main_node.id"))
    comments = db.relationship("Otofun_Comment", backref="thread", lazy=True)


class Otofun_Comment(db.Model):
    __tablename__ = "otofun_comment"

    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String)
    date = db.Column(db.Date)
    order = db.Column(db.Integer)
    content = db.Column(db.Text)
    tokenized_text = db.Column(db.String)
    prediction = db.Column(db.String)

    thread_id = db.Column(db.Integer, db.ForeignKey("otofun_thread.id"))


class Vnf_Bank(db.Model):
    __tablename__ = "vnf_bank"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.Date)
    content = db.Column(db.Text)
    tokenized_text = db.Column(db.String)
    prediction = db.Column(db.String)


class Cafef_Bank(db.Model):
    __tablename__ = "cafef_bank"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    subject = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.Date)
    content = db.Column(db.Text)
    tokenized_text = db.Column(db.String)
    prediction = db.Column(db.String)


class Cafef_Company(db.Model):
    __tablename__ = "cafef_company"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    subject = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.Date)
    content = db.Column(db.Text)
    tokenized_text = db.Column(db.String)
    prediction = db.Column(db.String)


class Cafef_Stock(db.Model):
    __tablename__ = "cafef_stock"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    subject = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.Date)
    content = db.Column(db.Text)
    tokenized_text = db.Column(db.String)
    prediction = db.Column(db.String)


class Dantri_Business(db.Model):
    __tablename__ = "dantri_business"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    subject = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.Date)
    content = db.Column(db.Text)
    tokenized_text = db.Column(db.String)
    prediction = db.Column(db.String)