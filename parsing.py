import requests
from bs4 import BeautifulSoup
import lxml
import json


def get_response(url):
    response = requests.get(url)
    return response.text
    # comment


def get_soup(html):
    return BeautifulSoup(html, "lxml")
    # comment


def get_page(html):
    soup = get_soup(html)
    page = soup.find("div", class_="elementor-column elementor-col-50 elementor-top-column elementor-element "
                                   "elementor-element-795124c").find_all("article")
    return page
    # comment


def get_inside(link):
    detail = get_response(link)
    soup = get_soup(detail)

    inside = soup.find("div", class_="stk-post stk-layout_12col_4805 stk-theme_45702 wp-exclude-emoji").text
    return inside
    # comment


def get_data(page):
    i = 1
    result = {}
    for item in page:

        html_title = item.find("h3", class_="elementor-post__title").text.split()
        title = " ".join(html_title)

        link = item.find("a").get("href")
        description = get_inside(link)

        img = item.find("img").get("src")

        data = {"title": title, "description": description, "img": img}
        result[i] = data
        i += 1

    return result
    # comment


def get_write(data):
    with open("news.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def start_pars():
    url = "https://kloop.kg/news/"

    html = get_response(url)
    page = get_page(html)

    data = get_data(page)
    get_write(data)


if __name__ == '__main__':
    start_pars()
