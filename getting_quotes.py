import requests
import pandas as pd
from bs4 import BeautifulSoup

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

# загрузка данных о котировках
res = requests.get('https://mfd.ru/marketdata/?id=5&group=16&mode=3&sortHeader=name&sortOrder=1&selectedDate=01.11.2019')
# данные из запроса обрабатываются с помощью Beautifulsoup в виде html контента
html = BeautifulSoup(res.content, features="lxml")
# выборка части кода включающего тег <table> с названием класса в котором заключается информация с котировками
table = html.find('table', {'class': 'mfd-table'})
# пустой список
rows = []
trs = table.find_all('tr') # выборка части кода с тегами <tr> из <table>
# выборка текстовой информации из полученной html таблицы в список
for tr in trs:
    tr = [td.get_text(strip=True) for td in tr.find_all('td')]
    if len(tr) > 0:
        rows.append(tr)
# загружаем данные из списка во фрейм pandas с названием столбцов
data = pd.DataFrame(rows, columns=['Тикер', 'Дата', 'Сделки_сумма', 'Сделки_ед', 'Сделки_%', 'Перед_закр', 'откр', 'мин', 'макс', 'срвзв', 'объем_шт', 'объем_руб', 'кол_сделок'], )
# выборка данных по сумме сделок с заполненными строками
data = data[data['Сделки_сумма'] != 'N/A']
# замена мешающих символов
data['Сделки_%'] = data['Сделки_%'].str.replace('−', '-').str.replace('%', '').astype('float')
# назначение индекса
data = data.set_index('Сделки_%')
# сортировка по индексу в порядке убывания
data = data.sort_index(ascending=False)
# сброс индекса
data = data.reset_index()
# вывод информации по тикеру первой строки (ответ)
print(data['Тикер'][0:1])
