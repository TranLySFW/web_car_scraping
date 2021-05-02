import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from database.tables import *


def cafef_get_list_articles_main_page(number_of_loading=5):
    """
    Retrieve all links of articles on main page of tinhte

    :number_of_loading: how many times we push the button
    :return: list of articles
    """
    try:
        list_articles = []  # set output
        driver = webdriver.Firefox()  # using selenium with Firefox
        driver.get(main_page_url)  # get main page of Tinhte
    except Exception as e:
        print(f"[Get page] Cannot get content of page!, error code {e}")
        return None

    try:
        button_more = driver.find_element_by_xpath("//button[contains(@class, 'load-more-btn')]")  # search button to load more

        if not button_more:  # reserved
            print(f"There is only one page!")
        else:
            for i in range(0, number_of_loading):  # count action of clicking
                print(f"Clicked: {i + 1} times")
                try:
                    button_more.click()  # simulated clicking
                    wait = ui.WebDriverWait(driver, timeout=20)  # wait for browser to load
                    wait.until(lambda driver: driver.find_element_by_xpath("//button[contains(@class, 'load-more-btn')]"))
                except Exception as e:
                    print(f"[Load more articles] Error code {e}")
                    continue

    except Exception as e:
        print(f"[Handle click] Error code {e}")

    try:
        articles = driver.find_elements_by_tag_name("article")  # find articles
        if not articles:
            print("None")

        for article in articles:
            a_tag = article.find_elements_by_tag_name("a")

            if a_tag:
                # print(a_tag[0].get_attribute("href"))
                list_articles.append(a_tag[0].get_attribute("href"))

        articles.clear()
        driver.close()
        print(f"The number of articles are collected: {len(list_articles)}")
        return list_articles

    except Exception as e:
        print(f"[Get articles] Error code {e}")