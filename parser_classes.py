"""Парсер сайтов на основе классов для новостного ТГ бота"""
import config
import requests
from bs4 import BeautifulSoup

links = config.resources  # список ссылок на ресурсы

# заголовки для иммитации реального пользователя
headers = {
    "accept": "*/*",
    "user-agent": ""
}


def titles_pars(titles):
    """Поиск и добавление заголовков в список"""
    if titles:
        title_list = []  # список чистых заголовков

        for title in titles:
            title_list.append(title.text)  # получаем текст заголовка

        return title_list


def links_parse(articles):
    article_list = []  # список ссылок на статьи

    for article in articles:
        article_url = article.get("href")  # получаем ссылку из тега
        article_list.append(article_url)

    return article_list


class MyParser:

    def __init__(self, resource, key_word):
        self.url = links[resource] + key_word  # собираем ссылку с поисковым запросом
        self.req = requests.get(self.url, headers=headers)
        self.src = self.req.text
        self.soup = BeautifulSoup(self.src, 'lxml')


class RbcParse(MyParser):

    def __init__(self, k_word):
        super().__init__(0, key_word=k_word)
        # Собираем заголовки со страницы РБК
        self.titles = self.soup.find_all("span", class_="search-item__title", limit=5)
        # Собираем ссылки на статьи со страницы РБК
        self.articles = self.soup.find_all("a", class_='search-item__link', limit=5)

    def rbc_parse(self):

        title_list = titles_pars(self.titles)
        if self.titles:
            article_list = links_parse(self.articles)

            dicty = dict(zip(title_list, article_list))  # создаем словарь {заголовок: ссылка}

            return dicty

        elif not self.titles:
            return "No articles with this word today on RBK"


class RiaParse(MyParser):

    def __init__(self, k_word):
        super().__init__(1, key_word=k_word)
        # Собираем заголовки со страницы РИА
        self.titles = self.soup.find_all("a", class_="list-item__title", limit=5)
        # Собираем ссылки на статьи со страницы РИА
        self.articles = self.soup.find_all("a", class_="list-item__title", limit=5)

    def ria_parse(self):
        title_list = titles_pars(self.titles)
        if self.titles:
            article_list = links_parse(self.articles)

            dicty = dict(zip(title_list, article_list))  # создаем словарь {заголовок: ссылка}

            return dicty

        elif not self.titles:
            return "No articles with this word today on RIA"
