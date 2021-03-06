import requests
import time
import numpy as np
from bs4 import BeautifulSoup

from joblib import load
import torch
from transformers import AutoModel, AutoTokenizer

from database.tables import *

service = 'http://localhost:7000/v1/segmenting?skipPunct=1'

# Start container of vncorenlp in docker with port 8000
# >> docker run -d -p 7000:8080 ndthuan/vi-word-segmenter:latest


# lr_clf = load('D:\\02_projects\\06_web_car__scrape\\web_car_scraping\\lr_clf.joblib')
# phobert = AutoModel.from_pretrained("vinai/phobert-large")
# tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-large", use_fast=False)

def muse_get_prediction(feature):
    """
    predict sentiment from vector

    :param feature:
    :return:
    """
    prediction = lr_clf.predict([feature])
    map_result = {0: 'Positive',
                  1: 'Negative'}
    return map_result[prediction[0]]


def muse_tokenize_data(text):
    """
    text -> vncorenlp -> phoBert -> vector 1024 items of float

    :param text: input text
    :return: vector
    """
    request_data = {"text": text}                           # request data
    result = requests.post(service, json=request_data)      # post to service vncorenlp
    data = result.json()                                    # get json of sentences
    sentences = ' '.join(data['sentences'])                 # connect sentences
    tokenized = torch.tensor([tokenizer.encode(sentences)]) # use phoBert to extract information
    tokenized = tokenized[:, :256]                          # truncate part of the tokenized sentences since model only accept  at most 256 vector size

    with torch.no_grad():
        last_hidden_states = phobert(tokenized)

    feature = last_hidden_states[0][:, 0, :].numpy().flatten()
    return feature


def muse_tinhte_predict():
    """
    Update comments with prediction in database
    :return:
    """
    for i in range(1, 121100):                                                  # id_start and id_stop
        try:
            print(f"Processing id = {i}")
            comment_instance = Tinhte_Comment.query.filter_by(id=i).first()     # get comment
            tokenized_text = muse_tokenize_data(comment_instance.comment)       # vectorization
            sentiment = muse_get_prediction(tokenized_text)                     # classification
            comment_instance.tokenized_text = str(tokenized_text)               # save to db
            comment_instance.prediction = sentiment                             # get sentiment to db

            db.session.commit()
        except Exception as e:
            print(f"error {e}")
            continue

    return None


def muse_vnf_predict():
    for i in range(1, 4300):  # id_start and id_stop
        try:
            print(f"Processing id = {i}")
            article_instance = Vnf_Bank.query.filter_by(id=i).first()  # get comment
            tokenized_text = muse_tokenize_data(article_instance.title)  # vectorization
            sentiment = muse_get_prediction(tokenized_text)  # classification
            article_instance.tokenized_text = str(tokenized_text)  # save to db
            article_instance.prediction = sentiment  # get sentiment to db

            db.session.commit()
        except Exception as e:
            print(f"error {e}")
            continue

    return 1


def muse_dantri_predict():
    for i in range(1, 2220):  # id_start and id_stop
        try:
            print(f"Processing id = {i}")
            article_instance = Dantri_Business.query.filter_by(id=i).first()  # get comment
            tokenized_text = muse_tokenize_data(article_instance.title)  # vectorization
            sentiment = muse_get_prediction(tokenized_text)  # classification
            article_instance.tokenized_text = str(tokenized_text)  # save to db
            article_instance.prediction = sentiment  # get sentiment to db

            db.session.commit()
        except Exception as e:
            print(f"error {e}")
            continue

    return 1

if (__name__ == "__main__"):
    # service = 'http://localhost:8000/v1/segmenting?skipPunct=1'
    # request_data = """L???i d???ng d???ch b???nh ph???c t???p, l??m ??n kh?? kh??n, c???n t???t ng?????i d??n c???n ti???n, c??c s??n ch???ng kho??n ph??i sinh qu???c t???, Forex tr??? n??n l???ng h??nh. ??i l???a gi??o vi??n, nh??n vi??n v??n ph??ng, ng?????i v??? h??u v?? c??? t??i x??? xe ??m t??? v??i ch???c tri???u ?????n c??? t??? ?????ng."""
    #
    # tokenized_text = muse_tokenize_data(request_data)
    # print(tokenized_text)
    # print(len(tokenized_text))
    # result = muse_get_prediction(tokenized_text)
    # print(result)
    muse_tinhte_predict()
