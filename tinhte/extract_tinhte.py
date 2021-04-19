import requests
import re
from bs4 import BeautifulSoup

xe_tinhte_url = "https://xe.tinhte.vn/"
MAX_PAGINATION = 100

def tinhte_get_list_articles():
    """
    Get list of articles in url

    :return: list of links of articles on main page
    """
    try:
        # xe_tinhte_url = "https://xe.tinhte.vn/"
        full_url = f"{xe_tinhte_url}"  # URL & Headers
        print(f"Page: {full_url}")  # full URL in case of prefix

        list_articles = []

        res = requests.get(full_url)  # get html content
        if (res.status_code) != 200:
            print("Can not get page, please check url!")
            return False

        bs_object = BeautifulSoup(res.text, 'html.parser')  # page content
        articles = bs_object.find_all("div", attrs={"class": ["article", "item"]})

        for article in articles:
            a_tag = article.find("a")

            if a_tag:
                list_articles.append(a_tag['href'])

        print(list_articles)
        return list_articles

    except Exception as e:
        print(f"ERROR:  {e}")
        return False


def tinhte_get_content_article(article_url):
    """
    Get useful information from article

    :param article:
    :return:
    """
    try:
        title, content, comments = "", "", []

        res = requests.get(article_url)
        if (res.status_code) != 200:
            print("Can not get page, please check url!")
            return False

        bs_object = BeautifulSoup(res.text, 'html.parser')  # html content
        print(f"article url: {article_url}")

        title_obj = bs_object.find("div", attrs={"class": ["thread-title"]})  # get title of article
        if title_obj:
            title = title_obj.text

        content_object = bs_object.find("article", attrs={"class": ["content"]})
        if content_object:
            content = content_object.text
            content = content.replace("\n", "")
            # print(article_content)

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

        # print(comments)

        return {"title": title,
                "content": content,
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
    list_articles = tinhte_get_list_articles()
    tinhte_get_content(list_articles)
