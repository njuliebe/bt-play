# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

bt_galaxy = 'http://btgalaxy.com/'
proxies = {'http': '127.0.0.1:1087'}


def search_movie(movie_name):
    movie_items = []

    url = bt_galaxy + '?s=' + movie_name
    res = requests.get(url=url, proxies=proxies)
    content = res.text
    soup = BeautifulSoup(content, "lxml")
    articles = soup.find_all('article')

    for article in articles[1:]:
        size_div = article.find('div', class_='entry-meta')
        size = size_div.contents[0]
        href = article.h2.a['href']
        name = article.h2.a.contents[0]
        href = bt_galaxy + href[1:]

        item = {
            'name' : name,
            "size" : size,
            "href" : href
        }
        movie_items.append(item)

    return movie_items


def get_magnet(url):
    res = requests.get(url=url, proxies=proxies)
    soup = BeautifulSoup(res.text, 'lxml')
    download_items = soup.find_all('i', class_='material-icons md-18')
    magnet_url = download_items[1].parent.a['href']
    return magnet_url


if __name__ == "__main__":
    movie_name = '华盛顿邮报'
    items = search_movie(movie_name)
    print items[0].get('name')
    url = items[0].get('href')
    print get_magnet(url)
