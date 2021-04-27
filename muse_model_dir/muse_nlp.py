import requests
import time
import numpy as np
from bs4 import BeautifulSoup

from joblib import load
import torch
from transformers import AutoModel, AutoTokenizer

from database.tables import *

service = 'http://localhost:8000/v1/segmenting?skipPunct=1'


# Start container of vncorenlp in docker with port 8000
# >> docker run -d -p 8000:8080 ndthuan/vi-word-segmenter:latest


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


if (__name__ == "__main__"):
    # service = 'http://localhost:8000/v1/segmenting?skipPunct=1'
    # request_data = """Lợi dụng dịch bệnh phức tạp, làm ăn khó khăn, cận tết người dân cần tiền, các sàn chứng khoán phái sinh quốc tế, Forex trở nên lộng hành. Đi lừa giáo viên, nhân viên văn phòng, người về hưu và cả tài xế xe ôm từ vài chục triệu đến cả tỉ đồng."""
    #
    # tokenized_text = muse_tokenize_data(request_data)
    # print(tokenized_text)
    # print(len(tokenized_text))
    # result = muse_get_prediction(tokenized_text)
    # print(result)
    muse_tinhte_predict()
