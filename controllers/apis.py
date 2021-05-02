from main import app
from main import db
import json

from tinhte.extract_tinhte import *
from muse_model_dir.muse_nlp import *
from otofun.extract_otofun import *
from vietnamfinance.extract_vnf import *


@app.route('/')
def hello():
    return "Welcome to Muse Media"


@app.route('/drop')
def drop_all():
    db.drop_all()
    return "Delete all tables"


@app.route('/write_db')
def write_db_all():
    # list_nodes = otofun_get_main_nodes()
    # flag = ototfun_get_threads(list_nodes)
    # flag = otofun_get_comments_to_db()
    flag = vnf_get_bank_articles()

    if flag:
        return "Success"
    else:
        return "Fail"




@app.route('/predict')
def predict_comment():
    muse_tinhte_predict()
    return "1"
