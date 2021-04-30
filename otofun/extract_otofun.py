import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from database.tables import *


def otofun_get_main_nodes():
    """
    Retrieve all links of articles on main page of otofun

    :number_of_loading: how many times we push the button
    :return: list of articles
    """
    main_page_url = "https://www.otofun.net/forums/"

    try:
        list_nodes = []  # set output
        driver = webdriver.Firefox()  # using selenium with Firefox
        driver.get(main_page_url)  # get main page of Tinhte
    except Exception as e:
        print(f"[Get page] Cannot get content of page!, error code {e}")
        return None

    try:
        nodes = driver.find_elements_by_xpath(
            "//div[contains(@class, 'node-body')]//h3[contains(@class, 'node-title')]//a")  # find main nodes

        if nodes:
            for node in nodes:
                node_instance = Otofun_MainNode(url=node.get_attribute('href'), subject=node.text)
                db.session.add(node_instance)
                db.session.commit()
                list_nodes.append(node.get_attribute('href'))

        nodes = driver.find_elements_by_xpath("//div[contains(@class, 'node-subNodesFlat')]//a[contains(@class,'subNodeLink')]")
        if nodes:
            for node in nodes:
                if not(node.get_attribute('href') in list_nodes):
                    node_instance = Otofun_MainNode(url=node.get_attribute('href'), subject=node.text)
                    db.session.add(node_instance)
                    db.session.commit()
                    list_nodes.append(node.get_attribute('href'))

        nodes.clear()
        # list_nodes = (list(set(list_nodes)))

        for node in list_nodes:
            print(node)

        return list_nodes

    except Exception as e:
        print(f"[Get articles] Error code {e}")
    finally:
        driver.close()
        return None


def ototfun_get_threads(list_nodes):
    """

    :return:
    """
    main_page_url = "https://www.otofun.net/forums/"
    MAX_THREAD = 50  # number of active thread everyday

    try:
        list_active_threads = []
        for i, node in enumerate(list_nodes):
            print(f"processing node: {i}, thread URL: {node}")
            node_url = node
            for page in range(0, MAX_THREAD):

                if page:
                    node_url = node + f"/page-{page}"

                res = requests.get(node_url, timeout=5, allow_redirects=False)

                if (res.status_code) != 200:
                    print("Can not get page, please check url!")
                    continue

                bs_object = BeautifulSoup(res.text, 'html.parser')  # html content

                threads = bs_object.find_all("div", attrs={"class": ["structItem"]})

                for thread in threads:
                    title = thread.find("div", attrs={"class": ["structItem-title"]})
                    a_tag = title.find_all("a")

                    list_active_threads.append(main_page_url + a_tag[-1]["href"])
                    print(main_page_url + a_tag[-1]['href'])

                    last_update = thread.find("time", attrs={"class": ["structItem-latestDate"]})

                    if last_update:
                        data_time = (last_update['data-time-string'])  # 21:06
                        hour = data_time.split(":")[0]
                        minute = data_time.split(":")[1]
                        data_date = last_update['data-date-string']  # 24/3/21
                        day = data_date.split("/")[0]
                        month = data_date.split("/")[1]
                        year = last_update['datetime'].split("-")[0]  # 2021-03-24T17:09:58+0700
                        last_update = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))

                        print(last_update)

        return list_active_threads

    except Exception as e:
        print(f"ERROR: {e}")
        return False


def otofun_get_comments(thread_url):
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
            person, date, content, order = "", datetime(1970, 1, 1), "", 0

            content = article.find("div", attrs={"class": ["bbWrapper"]})

            quote = article.find("blockquote")
            if quote:
                quote.clear()

            embed = article.find("div", attrs={"class": ["bbCodeBlock"]})
            if embed:
                embed.clear()

            content = content.text.replace("\n", "")

            publish_date = article.find("div", attrs={"class": ["message-attribution-main"]})
            publish_date = publish_date.find("a")
            publish_date = publish_date.text.replace("\n", "").strip()
            # print(publish_date)
            hour = publish_date.split(" ")[0].split(":")[0]
            minute = publish_date.split(" ")[0].split(":")[1]
            day = publish_date.split(" ")[1].split("/")[0]
            month = publish_date.split(" ")[1].split("/")[1]
            year = publish_date.split(" ")[1].split("/")[2]

            date = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))

            order_of_comment = article.find("ul", attrs={"class": ["message-attribution-opposite message-attribution-opposite--list"]})
            order_of_comment = order_of_comment.find("a")
            if order_of_comment:
                order = int(order_of_comment.text.replace("\n", "").strip().split("#")[1])

            person = article.find("span", attrs={"class": "username--style2"})
            if person:
                person = person.text

            print(f"person: {person}, date = {date}, content = {content}, order = {order}")
        return 1

    except Exception as e:
        print(f"ERROR: {e}")
        return False


if (__name__ == "__main__"):
    otofun_get_main_nodes()
    # ototfun_get_threads(["https://www.otofun.net/forums/xe-cua-nam-2021.424/"])
    # otofun_get_comments()
