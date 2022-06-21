# загрузка результатов в БД

'''
Соберите данные о моделях холодильников Саратов с маркетплейса beru.ru: URL, название, цена, размеры, общий объем, объем холодильной камеры.
Создайте соответствующие таблицы в SQLite базе данных и загрузите полученные данные в таблицу beru_goods.
Для парсинга можно использовать зеркало страницы beru.ru с результатами для холодильников Саратов по адресу:
video.ittensive.com/data/018-python-advanced/beru.ru/
'''
# использовал сайт ситилинк, т.к. зеркало беру не работает, а сам сайт блокитует роботов

import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup

# получаем ссылки на страницы со всеми холодильниками Саратов
header = {'User-Agent': 'ittensive-python-scraper/1.0 (+https://ittensive.com)'} # информация для разработчиков объекта парсинга
# функция для выборки цифр из текста
def find_number (s):
    return int("0" + "".join(i for i in s if i.isdigit()))
# функция выбирающая нужные данные со страниц с холодильниками
def find_data (link):
    r = requests.get("https://www.citilink.ru" + link, headers=header)
    html = BeautifulSoup(r.content, features="lxml")
    title = html.find("h1", {"class": "Heading Heading_level_1 ProductHeader__title"}).get_text().split("                    ")[1].split("\n")[0]
    price = find_number(html.find("span", {"class": "ProductHeader__price-default_current-price js--ProductHeader__price-default_current-price"}).get_text())
    tags = html.find_all("div", {"class": "Specifications__row"})
    width = 0
    depth = 0
    heigh = 0
    volume_all = 0
    volume_ref = 0
    volume_freez = 0
    for tag in tags:
        if tag.get_text().find("Объем:") > -1:
            volume_all = find_number(tag.find("div", {"class": "Specifications__column Specifications__column_value"}).get_text().split(";")[0])
            volume_ref = find_number(tag.find("div", {"class": "Specifications__column Specifications__column_value"}).get_text().split(";")[1])
            volume_freez = find_number(tag.find("div", {"class": "Specifications__column Specifications__column_value"}).get_text().split(";")[2])
        if tag.get_text().find("Размеры (ШхВхГ):") > -1:
            width = find_number(tag.find("div", {"class": "Specifications__column Specifications__column_value"}).get_text().split("х")[0])
            depth = find_number(tag.find("div", {"class": "Specifications__column Specifications__column_value"}).get_text().split("х")[2])
            heigh = find_number(tag.find("div", {"class": "Specifications__column Specifications__column_value"}).get_text().split("х")[1])
    text_link = "https://www.citilink.ru" + link
    return [text_link, title, price, volume_all, volume_ref, volume_freez, width, depth, heigh]
# находим все ссылки на холодильники Саратов
r = requests.get("https://www.citilink.ru/catalog/holodilniki/SARATOV/", headers=header)
html = BeautifulSoup(r.content, features="lxml")
links = html.find_all("a", {"class": "ProductCardVertical__name Link js--Link Link_type_default"})
# выбираем все необходимые данные со страниц каждого холодильника
data = []
for link in links:
    if link["href"] and link.get_text().find("Саратов") > -1:
        data.append(find_data(link["href"]))
# работа с БД
conn = sqlite3.connect("sqlite/data.db3") # устанавливаем соединение с БД data
db = conn.cursor() # открываем базу данных для работы
'''
# создаем таблицу citilink_goods в БД (закоментировано, т.к. таблица уже создана)
db.execute("""CREATE TABLE citilink_goods
            (id INTEGER PRIMARY KEY AUTOINCREMENT not null,
            url text,
            title text default '',
            price INTEGER default 0,
            volume_all INTEGER default 0,
            volume_ref INTEGER default 0,
            volume_freez INTEGER default 0,
            width INTEGER default 0,
            depth INTEGER default 0,
            heigh INTEGER default 0)""")
conn.commit() # выполняем 
# добавляем все данные о холодильниках в таблицу citilink_goods
db.executemany("""INSERT INTO citilink_goods (url, title, price, volume_all, volume_ref, volume_freez, width, depth, heigh) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
conn.commit() # выполняем'''

# выбираем данные во фрейм пандас из таблицы citilink_good БД data
data = pd.read_sql_query("""SELECT * FROM citilink_goods""", conn)
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

print(data) # выводим данные на экран
db.close() # закрываем БД
