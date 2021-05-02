from flask import Flask
from database.tables import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:zxcvbnm1@localhost/muse_media"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.app = app
db.init_app(app)

from tinhte.extract_tinhte import *
from muse_model_dir.muse_nlp import *
from otofun.extract_otofun import *
from vietnamfinance.extract_vnf import *
# from telegram.extract_telegram import *
from controllers.apis import *

if (__name__ == "__main__"):
    db.create_all()
    app.run()
