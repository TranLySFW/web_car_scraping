import requests
import time
import re
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from database.tables import *


def cafef_get_list_articles_main_page(number_of_loading=100):
    """
    Retrieve all links of articles on main page of tinhte

    :number_of_loading: how many times we push the button
    :return: list of articles
    """

    # main_page_url = "https://cafef.vn/tai-chinh-ngan-hang.chn"
    # main_page_url = "https://cafef.vn/doanh-nghiep.chn"
    main_page_url = "https://cafef.vn/thi-truong-chung-khoan.chn"

    try:
        list_articles = []  # set output
        driver = webdriver.Firefox()  # using selenium with Firefox
        driver.get(main_page_url)  # get main page of cafef
    except Exception as e:
        print(f"[Get page] Cannot get content of page!, {e}")
        return None

    try:
        html = driver.find_element_by_tag_name('html')
        for j in range(0, number_of_loading):
            print(f"Clicked: {j + 1} times")
            button_more = ""
            for i in range(0, 10):
                html.send_keys(Keys.END)
                time.sleep(3)
                try:
                    button_more = driver.find_element_by_xpath("//div[contains(@class,'bt_xemthem')]//a[contains(@class, 'sprite')]")
                    if button_more:
                        break
                except:
                    continue

            try:
                button_more.click()
            except Exception as e:
                print(f"[Testing click] {e}")
                continue

    except Exception as e:
        print(f"[Handling click] {e}")

    try:
        articles = driver.find_elements_by_xpath("//li[contains(@class, 'tlitem')]//h3//a")  # find articles
        if not articles:
            print("None")

        print(f"Number of article: {len(articles)}")
        for article in articles:
            # print(f"article: {article.get_attribute('title')}")
            print(f"article: {article.get_attribute('href')}")
            list_articles.append(article.get_attribute("href"))

        articles.clear()
        driver.close()
        with open("cafef_article.txt", "w") as f:
            for item in list_articles:
                f.write(item + "\n")
        return list_articles

    except Exception as e:
        print(f"[Get articles] Error code {e}")


def cafef_write_articles_to_db():
    with open("D:\\02_projects\\06_web_car__scrape\\web_car_scraping\\cafef\\cafef_article.txt", "r+") as f:
        link_articles = f.read().splitlines()
    # print(link_articles)

    for article in link_articles:
        article_existed = Cafef_Stock.query.filter_by(url=article).first()
        if article_existed:
            print(f"article existed")
            continue
        else:
            print(f"article url {article}")

        article_instance = Cafef_Stock(url=article)
        db.session.add(article_instance)
        db.session.commit()

    return 1


def cafef_get_content_article():
    for i in range(1, 1135):
        print(f"processing id: {i}")
        article = Cafef_Stock.query.filter_by(id=i).first()

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

        bs_object = BeautifulSoup(res.text, 'html.parser')  # html content

        title_obj = bs_object.find("h1", attrs={"class": ["title"]})
        if title_obj:
            title = title_obj.text.replace("\n", "").strip()
            # print(title)

        date_obj = bs_object.find("span", attrs={"class": ["pdate"]})
        if date_obj:  # 03-05-2021 - 07:42 AM
            print(date_obj.text)
            day_month_year, hour_minute = date_obj.text.split(" - ")
            hour = hour_minute.split(" ")[0].split(":")[0]
            minute = hour_minute.split(" ")[0].split(":")[1]
            day = day_month_year.split("-")[0]
            month = day_month_year.split("-")[1]
            year = day_month_year.split("-")[2]

            date_info = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
            # print(date_info)

        subject_obj = bs_object.find("a", attrs={"class": ["cat"]})
        if subject_obj:
            subject = subject_obj.text.replace("\n", "")
            # print(subject)

        open_content = bs_object.find("h2", attrs={"class": ["sapo"]})
        if open_content:
            open_content = open_content.text.replace("\n", "").strip()
        else:
            open_content = ""

        main_content = bs_object.find("span", attrs={"id": ["mainContent"]})
        if main_content:
            p_content = main_content.find_all("p")
            # print(p_content)
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


        # print(f"content: {open_content}")

        author_obj = bs_object.find("p", attrs={"class": ["author"]})
        if author_obj:
            author = author_obj.text

            # print(f"author: {author}")

        article.title = title
        article.subject = subject
        article.author = author
        article.date = date_info
        article.content = open_content
        db.session.add(article)
        db.session.commit()

    return 1



if (__name__ == "__main__"):
    cafef_get_list_articles_main_page()
    # cafef_get_content_article()
