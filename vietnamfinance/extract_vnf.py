import requests
import re
import datetime
# from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from database.tables import *


def vnf_get_bank_articles():
    """
    Retrieve all links of articles on main page of vietnamfinance

    :number_of_loading: how many times we push the button
    :return: list of articles
    """
    main_page_url = "https://vietnamfinance.vn/ngan-hang.htm"
    # https://vietnamfinance.vn/ngan-hang-p210.htm
    list_articles = []

    for page in range(145, 250):
        page_url = "https://vietnamfinance.vn/ngan-hang-p" + f"{page}" + ".htm"
        print(f"page_url: {page_url}")

        res = requests.get(page_url, timeout=20, allow_redirects=False)
        if (res.status_code) != 200:
            print(f"Can not get page, please check url: {page_url}!")
            continue

        try:
            bs_object = BeautifulSoup(res.text, 'html.parser')  # html content
            articles = bs_object.find_all("div", attrs={"class": ["timeline-item"]})

            for article in articles:
                a_tag = article.find("a")
                article_existed = Vnf_Bank.query.filter_by(url=a_tag['href']).first()
                if article_existed:
                    print(f"article existed: {a_tag['href']}")
                    continue
                # print(f"Title: {a_tag['title']}")
                # print(f"URL: {a_tag['href']}")

                article_url = a_tag['href']
                print(f"processing article: {article_url}")

                author_obj = article.find("span", attrs={"class": ["author-name"]})
                # print(f"Author: {author_obj.text}")
                author = author_obj.text

                date_info_obj = article.find("span", attrs={"class" :["article-info"]})
                author_obj.clear()
                date_info = date_info_obj.text.replace("\n", "").strip()
                # print(f'Date: {date_info}')
                if date_info:
                    hour_minute, day_month_year = date_info.split(", ")
                    hour = hour_minute.split(":")[0]
                    minute = hour_minute.split(":")[1]
                    day = day_month_year.split("/")[0]
                    month = day_month_year.split("/")[1]
                    year = day_month_year.split("/")[2]

                    date_info = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))

                # print(f'Date: {date_info}')

                res = requests.get(article_url, timeout=20, allow_redirects=False)
                if (res.status_code) != 200:
                    print(f"Can not get page, please check url: {article_url}!")
                    continue

                article_paper = BeautifulSoup(res.text, 'html.parser')  # html content

                open_content = article_paper.find("h2", attrs={"class": ["news-sapo"]})
                if open_content:
                    open_content = open_content.text.replace("\n", "").strip()
                else:
                    open_content = ""

                main_content = article_paper.find("div", attrs={"class": ["news-body-content"]})
                p_content = main_content.find_all("p")
                # print(p_content)

                for p_tag in p_content:
                    img_content = p_tag.find("img")
                    if img_content:
                        img_content.clear()
                    em_content = p_tag.find("em")
                    if em_content:
                        em_content.clear()

                    content = p_tag.text
                    open_content = open_content + "\n" + content

                # print(f"Content: {open_content}")

                article_instance = Vnf_Bank(url=a_tag['href'], title=a_tag['title'],
                                            date=date_info, author=author,
                                            content=open_content)
                db.session.add(article_instance)
                db.session.commit()

        except Exception as e:
            print(f"{e}")
            continue

    return 1

if (__name__ == "__main__"):
    vnf_get_bank_articles()