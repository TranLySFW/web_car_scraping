import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

main_page_url = "https://tinhte.vn/"
xe_tinhte_url = "https://xe.tinhte.vn/"
MAX_PAGINATION = 100


def tinhte_get_list_articles_main_page(number_of_loading=5):
    """
    Retrieve all links of articles on main page of tinhte

    :return: list of articles
    """
    try:
        list_articles = []
        driver = webdriver.Firefox()
        driver.get(main_page_url)
    except Exception as e:
        print(f"[Get page] Cannot get content of page!, error code {e}")
        return None

    try:
        button_more = driver.find_element_by_xpath("//button[contains(@class, 'load-more-btn')]")

        if not button_more:
            print(f"There is only one page!")
        else:
            for i in range(0, number_of_loading):
                print(f"Clicked: {i + 1} times")
                try:
                    button_more.click()
                    wait = ui.WebDriverWait(driver, timeout=20)
                    wait.until(lambda driver: driver.find_element_by_xpath("//button[contains(@class, 'load-more-btn')]"))
                except Exception as e:
                    print(f"[Load more articles] Error code {e}")
                    continue

    except Exception as e:
        print(f"[Handle click] Error code {e}")

    try:
        articles = driver.find_elements_by_tag_name("article")
        if not articles:
            print("None")

        for article in articles:
            a_tag = article.find_elements_by_tag_name("a")

            if a_tag:
                print(a_tag[0].get_attribute("href"))
                list_articles.append(a_tag[0].get_attribute("href"))

        articles.clear()
        driver.close()
        print(f"The number of articles are collected: {len(list_articles)}")
        return list_articles

    except Exception as e:
        print(f"[Get articles] Error code {e}")


def tinhte_get_list_articles_car_section():
    """

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




def tinhte_get_content_article(article_url):
    """
    Get useful information from article

    :param article:
    :return:
    """
    try:
        subject, date, title, content, tags, comments = "", datetime.today(), "", "", [], []

        res = requests.get(article_url)
        if (res.status_code) != 200:
            print("Can not get page, please check url!")
            return False

        bs_object = BeautifulSoup(res.text, 'html.parser')  # html content
        print(f"article url: {article_url}")

        subject_obj = bs_object.find_all("a", attrs={"class": ["label"]})
        if subject_obj:
            subject = subject_obj[-1].text
            print(f"subject: {subject}")

        date_obj = bs_object.find("span", attrs={"class": ["date"]})
        if date_obj:
            date = date_obj.text
            previous_day = 1
            if date in [ str(i) + "h" for i in range(0, 25)]:
                previous_day = datetime.today()
            else:
                date_symbol = date.split()[-1]
                if date_symbol == "ngày":
                    previous_day = int(date.split()[0])
                elif date_symbol == "tháng":
                    previous_day = int(date.split()[0]) * 30

            publish_date = datetime.today() - timedelta(previous_day)
            date = publish_date
            print(f"publish_date: {publish_date}")

        title_obj = bs_object.find("div", attrs={"class": ["thread-title"]})  # get title of article
        if title_obj:
            title = title_obj.text
            print(f"title: {title}")

        content_object = bs_object.find("article", attrs={"class": ["content"]})
        if content_object:
            content = content_object.text
            content = content.replace("\n", "")
            # print(article_content)

        tags_obj = bs_object.find_all("a", attrs={"class": ["tag"]})
        if tags_obj:
            for tag in tags_obj:
                tags.append(tag.text)
                print(tag.text)

        for i in range(1, MAX_PAGINATION):
            page_url = f"{article_url}page-{i}"
            print(f"page_url {page_url}")

            res = requests.get(page_url)
            if (res.status_code) != 200:
                print(f"End of pages")
                break

            bs_object = BeautifulSoup(res.text, 'html.parser')  # html content
            comment_divs = bs_object.find_all("div", attrs={"class": ["thread-comment__content"]})
            for comment_div in comment_divs:
                comment = comment_div.find("span")

                if comment:
                    text = comment.text
                    if text[0] != "@" and text[0] != " ":
                        comments.append(text)

        for comment in comments:
            print(comment)

        return {"subject": subject,
                "date": date,
                "title": title,
                "content": content,
                "tags": tags,
                "comments": comments}

    except Exception as e:
        print(f"ERROR: {e}")
        return False


def tinhte_get_content(list_articles):
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


if (__name__ == "__main__"):
    # list_articles = tinhte_get_list_articles()
    # tinhte_get_content(list_articles)
    # tinhte_get_list_articles_main_page(70)
    tinhte_get_content_article(
        "https://tinhte.vn/thread/triumph-ra-mat-street-scrambler-2022-dong-co-moi-ngoai-hinh-cai-tien-gia-tu-11-000-usd.3315725/")
