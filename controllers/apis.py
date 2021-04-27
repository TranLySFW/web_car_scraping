from main import app
from main import db
import json

from tinhte.extract_tinhte import *
from muse_model_dir.muse_nlp import *


@app.route('/')
def hello():
    return "Welcome to Muse Media"


@app.route('/drop')
def drop_all():
    db.drop_all()
    return "Delete all tables"


@app.route('/write_db')
def write_db_all():
    list_articles = tinhte_get_list_articles_main_page(number_of_loading=5)
    flag = tinhte_write_articles_to_db(list_articles)
    if flag:
        return "Success"
    else:
        return "Fail"


@app.route('/predict')
def predict_comment():
    muse_tinhte_predict()
    return "1"
