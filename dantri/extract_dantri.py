import requests
import time
import re
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from database.tables import *


def dantri_get_list_articles_main_page(number_of_loading=100):
    """
    Retrieve all links of articles on main page of tinhte

    :number_of_loading: how many times we push the button
    :return: list of articles
    """

    # main_page_url = "https://dantri.com.vn/kinh-doanh/tai-chinh-dau-tu.htm"
    # main_page_url = "https://dantri.com.vn/kinh-doanh/thi-truong.htm"
    main_page_url = "https://dantri.com.vn/kinh-doanh/doanh-nghiep.htm"


    list_articles = []  # set output
    try:
        for i in range(1, 31):
            try:
                page_url = f"https://dantri.com.vn/kinh-doanh/doanh-nghiep/trang-{i}.htm"
                print(f"processing i: {i}")
                print(f"page url: {page_url}")
                # article = Dantri_Business.query.filter_by(id=i).first()
                # if article.content:
                #     continue
                # else:
                #     article_url = article.url
                #     print(f"article url: {article_url}")

                res = requests.get(page_url, timeout=20, allow_redirects=False)
                if (res.status_code) != 200:
                    print(f"Can not get page, please check url: {page_url}!")
                    continue

                bs_object = BeautifulSoup(res.text, 'html.parser')  # html content

                main_div = bs_object.find("div", attrs={"class": ["dt-main-category"]})
                articles = main_div.find_all("h3", attrs={"class": ["news-item__title"]})
                for article in articles:
                    a_tag = article.find("a")
                    if a_tag:
                        # print(f"link: {'https://dantri.com.vn' + a_tag['href']}")
                        list_articles.append("https://dantri.com.vn" + a_tag['href'])
            except Exception as e:
                print(f"[Get list of article] {e}")

    except Exception as e:
        print(f"[Get page] {e}")

    with open("dantri_article.txt", "w") as f:
        for item in list_articles:
            f.write(item + "\n")

    return 1


def dantri_write_articles_to_db():
    with open("D:\\02_projects\\06_web_car__scrape\\web_car_scraping\\dantri\\dantri_article.txt", "r+") as f:
        link_articles = f.read().splitlines()
    # print(link_articles)

    for article in link_articles:
        article_existed = Dantri_Business.query.filter_by(url=article).first()
        if article_existed:
            print(f"article existed")
            continue
        else:
            print(f"article url {article}")

        article_instance = Dantri_Business(url=article)
        db.session.add(article_instance)
        db.session.commit()

    return 1


def dantri_get_content_article():
    for i in range(1, 5000):
        print(f"processing id: {i}")
        article = Dantri_Business.query.filter_by(id=i).first()

        if article.content:
            continue
        else:
            article_url = article.url
            print(f"article url: {article_url}")

        res = requests.get(article_url, timeout=20, allow_redirects=False)
        if (res.status_code) != 200:
            print(f"Can not get page, please check url: {page_url}!")
            continue

        title, date_info, subject, open_content, author = "", datetime.date(1970, 1, 1), "", "", ""
        try:
            bs_object = BeautifulSoup(res.text, 'html.parser')  # html content

            title_obj = bs_object.find("h1", attrs={"class": ["dt-news__title"]})
            if title_obj:
                title = title_obj.text.replace("\n", "").strip()
                # print(title)

            date_obj = bs_object.find("span", attrs={"class": ["dt-news__time"]})
            if date_obj:  #Thứ năm, 29/04/2021 - 20:08
                # print(date_obj.text)
                day_month_year, hour_minute = date_obj.text.split(" - ")
                day_month_year = day_month_year.split(", ")[1]

                hour = hour_minute.split(":")[0]
                minute = hour_minute.split(":")[1]
                day = day_month_year.split("/")[0]
                month = day_month_year.split("/")[1]
                year = day_month_year.split("/")[2]

                date_info = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
                # print(date_info)

            subject_obj = bs_object.find("ul", attrs={"class": ["dt-breadcrumb"]})
            subject_obj = subject_obj.find_all("li")[-1]
            subject_obj = subject_obj.find("a")
            if subject_obj:
                subject = subject_obj.text.replace("\n", "")
                # print(subject)

            open_content = bs_object.find("div", attrs={"class": ["dt-news__sapo"]})
            open_content = open_content.find("h2")
            if open_content:
                open_content = open_content.text.replace("\n", "").strip()
            else:
                open_content = ""

            main_content = bs_object.find("div", attrs={"class": ["dt-news__content"]})
            if main_content:
                p_content = main_content.find_all("p")
            #     # print(p_content)
                if p_content:
                    for p_tag in p_content:
                        img_content = p_tag.find("img")
                        if img_content:
                            img_content.clear()
                        em_content = p_tag.find("em")
                        if em_content:
                            em_content.clear()
                        div_content = p_tag.find("div")
                        if div_content:
                            div_content.clear()

                        content = p_tag.text
                        open_content = open_content + "\n" + content
                        author = p_tag.text # the last p tag in content

            # print(f"content: {open_content}")
            # print(f"author: {author}")

            article.title = title
            article.subject = subject
            article.author = author
            article.date = date_info
            article.content = open_content
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            print(f"{e}")
            continue

    return 1



if (__name__ == "__main__"):
    dantri_get_list_articles_main_page()

