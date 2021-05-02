import requests
import time
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from database.tables import *


def cafef_get_list_articles_main_page(number_of_loading=10):
    """
    Retrieve all links of articles on main page of tinhte

    :number_of_loading: how many times we push the button
    :return: list of articles
    """
    # SCROLL_PAUSE_TIME = 0.5
    # # Get scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     # Wait to load page
    #     time.sleep(SCROLL_PAUSE_TIME)
    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    main_page_url = "https://cafef.vn/tai-chinh-ngan-hang.chn"

    try:
        list_articles = []  # set output
        driver = webdriver.Firefox()  # using selenium with Firefox
        driver.get(main_page_url)  # get main page of cafef
    except Exception as e:
        print(f"[Get page] Cannot get content of page!, error code {e}")
        return None

    try:
        for j in range(0, number_of_loading):
            button_more = ""
            html = driver.find_element_by_tag_name('html')
            for i in range(0, 100):
                # html = driver.find_element_by_tag_name('html')
                html.send_keys(Keys.END)
                time.sleep(2)  # wait 2 seconds
                button_more = driver.find_element_by_xpath("//a[contains(@class, 'sprite')]")  # search button to load more
                if button_more:
                    break
            try:
                button_more.click()  # simulated clicking
                print(f"Clicked: {j + 1} times")
            except Exception as e:
                print(f"[Load more articles] {e}")
                continue

    except Exception as e:
        print(f"[Handle click] Error code {e}")

    try:
        articles = driver.find_elements_by_xpath("//li[contains(@class, 'tlitem')]//h3//a")  # find articles
        if not articles:
            print("None")

        for article in articles:
            print(f"article: {article.get_attribute('title')}")
            # list_articles.append(a_tag[0].get_attribute("href"))

        articles.clear()
        driver.close()
        # print(f"The number of articles are collected: {len(list_articles)}")
        return list_articles

    except Exception as e:
        print(f"[Get articles] Error code {e}")

if (__name__ == "__main__"):
    cafef_get_list_articles_main_page()