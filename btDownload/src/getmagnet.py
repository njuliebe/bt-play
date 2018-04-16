# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

bt_galaxy = 'http://btgalaxy.com/'

def searchMovie(movie_name):
    proxies = {'http':'127.0.0.1:1087'}
    url = bt_galaxy + '?s=' + movie_name
    res = requests.get(url=url, proxies=proxies)
    content = res.text
    soup = BeautifulSoup(content, "lxml")
    articles = soup.find_all('article')

    for article in articles[1:]:
        print article.find_all('div', class_='entry-meta')
        print article.h2

        # print article
        print type(article)



if __name__ == "__main__":
    movie_name = '肖申克'
    searchMovie(movie_name)
