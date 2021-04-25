import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from database.tables import *

main_page_url = "https://tinhte.vn/"
xe_tinhte_url = "https://xe.tinhte.vn/"
MAX_PAGINATION = 100


def tinhte_get_list_articles_main_page(number_of_loading=5):
    """
    Retrieve all links of articles on main page of tinhte

    :number_of_loading: how many times we push the button
    :return: list of articles
    """
    try:
        list_articles = []                              # set output
        driver = webdriver.Firefox()                    # using selenium with Firefox
        driver.get(main_page_url)                       # get main page of Tinhte
    except Exception as e:
        print(f"[Get page] Cannot get content of page!, error code {e}")
        return None

    try:
        button_more = driver.find_element_by_xpath("//button[contains(@class, 'load-more-btn')]")   # search button to load more

        if not button_more:                             # reserved
            print(f"There is only one page!")
        else:
            for i in range(0, number_of_loading):       # count action of clicking
                print(f"Clicked: {i + 1} times")
                try:
                    button_more.click()                 # simulated clicking
                    wait = ui.WebDriverWait(driver, timeout=20) # wait for browser to load
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


def tinhte_get_list_articles_car_section():
    """
    Retrieve all links of articles on car section of tinhte

    :return:
    """
    NUM_LOAD_MORE_ARTICLES = 20
    try:
        list_articles = []
        driver = webdriver.Firefox()
        driver.get(xe_tinhte_url)

        button_more = driver.find_element_by_xpath("//button[@type='button']")
        for i in range(0, NUM_LOAD_MORE_ARTICLES):
            print(f"i: {i}")
            try:
                button_more.click()
                wait = ui.WebDriverWait(driver, 20)
                wait.until(lambda driver: driver.find_element_by_xpath("//button[@type='button']"))
            except Exception as e:
                print(f"error {e}")

        articles = driver.find_elements_by_xpath("//div[contains(@class, 'article') or contains(@class, 'item')]")

        if not articles:
            print("None")

        for article in articles:
            a_tag = article.find_elements_by_tag_name("a")

            if a_tag:
                # print(a_tag[0].text)
                print(a_tag[0].get_attribute("href"))
                list_articles.append(a_tag[0].get_attribute("href"))

        articles.clear()
        driver.close()

        print(len(list_articles))

    except Exception as e:
        print(f"error {e}")


def tinhte_get_content_an_article(article_url):
    """
    Get useful information from  an article

    :param article_url:
    :return: dict of information
    """
    try:
        subject, date, title, content, tags, comments = "", datetime.today(), "", "", [], []

        res = requests.get(article_url, timeout=5)
        if (res.status_code) != 200:
            print("Can not get page, please check url!")
            return False

        bs_object = BeautifulSoup(res.text, 'html.parser')  # html content
        # print(f"article url: {article_url}")

        subject_obj = bs_object.find_all("a", attrs={"class": ["label"]})
        if subject_obj:
            subject = subject_obj[-1].text
            # print(f"subject: {subject}")

        date_obj = bs_object.find("span", attrs={"class": ["date"]})
        if date_obj:
            date = date_obj.text
            previous_day = 1

            if date in [str(i) + "h" for i in range(0, 25)]:
                publish_date = datetime.today()
            else:
                date_symbol = date.split()[-1]
                if date_symbol == "ngày":
                    previous_day = int(date.split()[0])
                elif date_symbol == "tháng":
                    previous_day = int(date.split()[0]) * 30

                publish_date = datetime.today() - timedelta(previous_day)

            date = publish_date
            # print(f"publish_date: {publish_date}")

        title_obj = bs_object.find("div", attrs={"class": ["thread-title"]})  # get title of article
        if title_obj:
            title = title_obj.text
            # print(f"title: {title}")

        content_object = bs_object.find("article", attrs={"class": ["content"]})
        if content_object:
            content = content_object.text
            content = content.replace("\n", "")
            # print(article_content)

        tags_obj = bs_object.find_all("a", attrs={"class": ["tag"]})
        if tags_obj:
            for tag in tags_obj:
                tags.append(tag.text)
                # print(tag.text)

        for i in range(1, MAX_PAGINATION):
            page_url = f"{article_url}page-{i}"
            # print(f"page_url {page_url}")

            res = requests.get(page_url)
            if (res.status_code) != 200:
                # print(f"End of pages")
                break

            bs_object = BeautifulSoup(res.text, 'html.parser')  # html content
            comment_divs = bs_object.find_all("div", attrs={"class": ["thread-comment__content"]})
            for comment_div in comment_divs:
                comment = comment_div.find("span")

                if comment:
                    text = comment.text
                    if text[0] != "@" and text[0] != " ":
                        comments.append(text)

        # for comment in comments:
        #     print(comment)

        return {"url": article_url,
                "subject": subject,
                "date": date,
                "title": title,
                "content": content,
                "tags": tags,
                "comments": comments}

    except Exception as e:
        print(f"ERROR: {e}")
        return False


def tinhte_get_content_list_articles(list_articles):
    """
    Get useful information from content of articles

    :param list_articles:
    :return:
    """
    try:
        result = []
        for article_url in list_articles:  # get list of articles
            result.append(tinhte_get_content_article(article_url))
        # print(result)
        return result

    except Exception as e:
        print(f"ERROR:  {e}")
        return False


def tinhte_write_an_article_to_db(observe):
    """
    Write an article from tinhte into database

    :return: 1 if okay
    """
    try:
        article_existed = Tinhte_Article.query.filter_by(url=observe["url"]).first()    # check existed

        if article_existed:
            current_comments = article_existed.comments                                 # get all existing comments
            if len(observe["comments"]) > len(current_comments):                        # compare number of comments
                for new_comment in observe["comments"]:
                    if not (new_comment in current_comments):
                        comment_instance = Tinhte_Comment(comment=new_comment)          # add more comments
                        article_existed.comments.append(comment_instance)

        else:
            article = Tinhte_Article(url=observe["url"],
                                     subject=observe["subject"],
                                     date=observe["date"],
                                     title=observe["title"],
                                     content=observe["content"])
            tags = observe["tags"]
            for tag in tags:
                tag_instance = Tinhte_Tag(tag=tag)
                article.tags.append(tag_instance)

            comments = observe["comments"]
            for comment in comments:
                comment_instance = Tinhte_Comment(comment=comment)
                article.comments.append(comment_instance)

            db.session.add(article)

        db.session.commit()
        return 1

    except Exception as e:
        print(f"Error writting, code {e}")
        return None


def tinhte_write_articles_to_db(list_articles):
    """
    Get useful information from content of articles

    :param list_articles:
    :return:
    """
    try:
        for i, article_url in enumerate(list_articles):  # get list of articles
            print(f"Processing url: {article_url}")
            print(f"at index i: {i} in {len(list_articles)}")
            observe = tinhte_get_content_an_article(article_url)
            success_flag = tinhte_write_an_article_to_db(observe)

            if not success_flag:
                print(f"Can not write to database with url: {article_url}")

        return 1

    except Exception as e:
        print(f"ERROR:  {e}")
        return None


if (__name__ == "__main__"):
    observe = tinhte_get_content_an_article(
        "https://tinhte.vn/thread/tong-hop-game-mobile-dang-chu-y-trong-tuan-3-thang-4-2021.3316747/")
    print(observe)
