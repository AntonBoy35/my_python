# Задание: получение котировок акций
'''
Получите данные по котировкам акций со страницы:
mfd.ru/marketdata/?id=5&group=16&mode=3&sortHeader=name&sortOrder=1&selectedDate=01.11.2019
и найдите, по какому тикеру был максимальный рост числа сделок (в процентах) за 1 ноября 2019 года.
'''

import requests
import pandas as pd
from bs4 import BeautifulSoup

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)
# загружаем данные о котировках
res = requests.get('https://mfd.ru/marketdata/?id=5&group=16&mode=3&sortHeader=name&sortOrder=1&selectedDate=01.11.2019')
# данные из запроса обрабатываем с помощью Beautifulsoup в виде html контента
html = BeautifulSoup(res.content, features="lxml")
table = html.find('table', {'class': 'mfd-table'})
# создаем пустой список
rows = []
trs = table.find_all('tr')
# перебираем внутри тега table все теги tr и внурти тегов tr теги td и добавляем данные в пустой список
for tr in trs:
    tr = [td.get_text(strip=True) for td in tr.find_all('td')]
    if len(tr) > 0:
        rows.append(tr)
# загружаем данные из списка во фрейм pandas с названием столбцов
data = pd.DataFrame(rows, columns=['Тикер', 'Дата', 'Сделки_сумма', 'Сделки_ед', 'Сделки_%', 'Перед_закр', 'откр', 'мин', 'макс', 'срвзв', 'объем_шт', 'объем_руб', 'кол_сделок'], )
# выбираем строки, где Сделки_сумма не равно N/A
data = data[data['Сделки_сумма'] != 'N/A']
# убираем лишние знаки
data['Сделки_%'] = data['Сделки_%'].str.replace('−', '-').str.replace('%', '').astype('float')
# назначаем индекс
data = data.set_index('Сделки_%')
# сортируем по индексу в порядке убывания
data = data.sort_index(ascending=False)
# убираем индекс
data = data.reset_index()
# выводим тикер первой строки (ответ)
print(data['Тикер'][0:1])
