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
    # загрузка данных с сайта по странично
    r = requests.get("https://www.citilink.ru" + link, headers=header)
    # преобразование response объекта в контент
    html = BeautifulSoup(r.content, features="lxml")
    # выборка данных с названием холодильника
    title = html.find("h1", {"class": "Heading Heading_level_1 ProductHeader__title"}).get_text().split("                    ")[1].split("\n")[0]
    # выборка данных с ценой холодильника
    price = find_number(html.find("span", {"class": "ProductHeader__price-default_current-price js--ProductHeader__price-default_current-price"}).get_text())
    # выборка данных заключенных в теги внутри блока класса "Specifications__row"
    tags = html.find_all("div", {"class": "Specifications__row"})
    width = 0
    depth = 0
    heigh = 0
    volume_all = 0
    volume_ref = 0
    volume_freez = 0
    # выборка данных из выбранного контента с объемом и размерами холодильников
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
# выбираем все необходимые данные со страниц с холодильниками
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
# проверка правильной загрузки данных в БД
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
