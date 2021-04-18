from flask import Flask
from MODEL.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:zxcvbnm1@localhost/storybee"
# app.config['SQLALCHEMY_DATABASE_URI']  = "postgresql+psycopg2://extractor:rkudfGRszmUJp88dpqBNh3r7@35.241.135.140:5432/storybee"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db.app = app
# db.init_app(app)

from tinhte.extract_tinhte import *
# from controllers.apis import *
# from controllers.update import *


if (__name__ == "__main__"):
    # db.create_all()
    app.run()
