import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from database.tables import *


MAX_PAGINATION = 100

def otofun_get_main_nodes():
    """
    Retrieve all links of articles on main page of otofun

    :number_of_loading: how many times we push the button
    :return: list of articles
    """
    main_page_url = "https://www.otofun.net/forums/"

    try:
        list_articles = []  # set output
        driver = webdriver.Firefox()  # using selenium with Firefox
        driver.get(main_page_url)  # get main page of Tinhte
    except Exception as e:
        print(f"[Get page] Cannot get content of page!, error code {e}")
        return None

    try:
        nodes = driver.find_elements_by_xpath("//div[contains(@class, 'node-body')]//h3[contains(@class, 'node-title')]//a")  # find main nodes
        print(type(nodes))

        if not nodes:
            print("None")

        for node in nodes:
            print(node.text)
            print(node.get_attribute("href"))

        nodes.clear()

        return 1

    except Exception as e:
        print(f"[Get articles] Error code {e}")
    finally:

        driver.close()


def ototfun_get_threads():
    """

    :return:
    """
    main_page_url = "https://www.otofun.net/"
    thread_url = "https://www.otofun.net/forums/xe-dop.216/"
    try:
        # subject, date, title, content, tags, comments = "", datetime.today(), "", "", [], []

        res = requests.get(thread_url, timeout=5)
        if (res.status_code) != 200:
            print("Can not get page, please check url!")
            return False

        bs_object = BeautifulSoup(res.text, 'html.parser')  # html content
        print(f"thread url: {thread_url}")

        threads = bs_object.find_all("div", attrs={"class": ["structItem-title"]})

        for thread in threads:
            a_tag = thread.find_all("a")
            print(main_page_url + a_tag[-1]["href"])


        return 1

    except Exception as e:
        print(f"ERROR: {e}")
        return False


def otofun_get_comments():
    """

    :return:
    """
    main_page_url = "https://www.otofun.net/"
    thread_url = "https://www.otofun.net/threads/xin-cac-cu-giup-ve-cai-khung-nay.1689818/"
    try:
        res = requests.get(thread_url, timeout=5, allow_redirects=False)
        if (res.status_code) != 200:
            print("Can not get page, please check url!")
            return False

        bs_object = BeautifulSoup(res.text, 'html.parser')  # html content
        print(f"thread url: {thread_url}")

        articles = bs_object.find_all("article", attrs={"class": ["message"]})
        # print(articles)

        for article in articles:
            person, date, content = "", datetime(1970, 1, 1), ""
            content = article.find("div", attrs={"class": ["bbWrapper"]})
            quote = article.find("blockquote")

            if quote:
                quote.clear()

            content = content.text.replace("\n", "")

            # publish_date = article.find("div", attrs={"class":["message-attribution-main"]})
            # publish_date = publish_date.find("a")
            # publish_date = publish_date.text.replace("\n", "").strip()
            #
            # hour = publish_date.strip(" ")[0].strip(":")[0]
            # minute = publish_date.strip(" ")[0].strip(":")[1]
            # day = publish_date.strip(" ")[1].strip(":")[0]
            # month = publish_date.strip(" ")[1].strip(":")[1]
            # year = publish_date.strip(" ")[1].strip(":")[2]
            #
            # date = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

            person = article.find("span", attrs={"class": "username--style2"})
            if person:
                person = person.text

            print(f"person: {person}, date = {date}")
        return 1

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if (__name__ == "__main__"):
    otofun_get_comments()