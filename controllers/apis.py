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
