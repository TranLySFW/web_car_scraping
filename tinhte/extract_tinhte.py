import requests
from bs4 import BeautifulSoup


def tinhte_get_list_articles():
    """
    Get list of articles in url

    :return:
    """
    try:
        # date_url = datetime.date(year, month, day).strftime("%Y%m%d")
        xe_tinhte_url = "https://xe.tinhte.vn/"

        full_url = f"{xe_tinhte_url}"  # URL & Headers
        print(f"Page: {full_url}")

        list_articles = []

        res = requests.get(full_url)
        if (res.status_code) != 200:
            print("Can not get page, please check url!")
            return False

        bs_object = BeautifulSoup(res.text, 'html.parser') # page content
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


def tinhte_get_content(list_articles):
    try:
        for article_url in list_articles:
            res = requests.get(article_url)
            if (res.status_code) != 200:
                print("Can not get page, please check url!")
                return False

            bs_object = BeautifulSoup(res.text, 'html.parser')
            print(f"article url: {article_url}")
            title = bs_object.find("div",  attrs={"class": ["thread-title"]})
            if title:
                print(title.text)

            article_content_object = bs_object.find("article", attrs={"class": ["content"]})
            if article_content_object:
                article_content = article_content_object.text
                article_content = article_content.replace("\n", "")
                # print(article_content)

            comments_objects = bs_object.find_all("div", attrs={"class": ["thread-comment__container"]})
            if comments_objects:

                for comment_obj in comments_objects:
                    # print(comment_obj)
                    main_comment_obj = comment_obj.find("div", attrs={"class": ["thread-comment__content"]})
                    print(main_comment_obj.text)


    except Exception as e:
        print(f"ERROR:  {e}")
        return False


if (__name__ == "__main__"):
    list_articles = tinhte_get_list_articles()
    tinhte_get_content(list_articles)