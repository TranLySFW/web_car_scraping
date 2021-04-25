from main import app
from main import db
import json

from tinhte.extract_tinhte import *


@app.route('/')
def hello():
    return "Welcome to Muse Media"


@app.route('/drop')
def drop_all():
    db.drop_all()
    return "Delete all tables"


@app.route('/write')
def write_one():
    row = tinhte_get_content_article(
        "https://tinhte.vn/thread/triumph-ra-mat-street-scrambler-2022-dong-co-moi-ngoai-hinh-cai-tien-gia-tu-11-000-usd.3315725/")
    tinhte_write_article_to_db(row)

    return "1"




@app.route('/update_xetinhte')
def update_xe_tinhte():
    list_articles = tinhte_get_list_articles()
    result = tinhte_get_content(list_articles)
    """
    TODO:
    1. Check existence of article in database
    2. Write content of article to database
    """
    return json.dumps(result)
