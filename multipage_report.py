# Задание: многостраничный отчет

'''
Используя данные по активностям в парках Москвы
https://video.ittensive.com/python-advanced/data-107235-2019-12-02.utf.json
Создайте PDF отчет, в котором выведите:
1. Диаграмму распределения числа активностей по паркам, топ10 самых активных
2. Таблицу активностей по всем паркам в виде Активность-Расписание-Парк
'''

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import binascii
import pdfkit
# гет запрос по ссылке
r = requests.get("https://video.ittensive.com/python-advanced/data-107235-2019-12-02.utf.json")
# выборка нужных столбцов json файла из response объекта
data = pd.DataFrame(json.loads(r.content),
                   columns=["CourseName", "CoursesTimetable", "NameOfPark"])
# выборка названий парков из набора словарей
data["NameOfPark"] = data["NameOfPark"].apply(lambda x: x["value"])
# переименование столбцов
data.columns = ["Активность", "Расписание", "Парк"]

# создание группированного и отсортированного датафрейма
parks = data.groupby("Парк").count().sort_values("Активность", ascending=False)
# отрисовка круговой диаграммы по активности в парках Москвы
fig = plt.figure(figsize=(12, 6))
area = fig.add_subplot(1, 1, 1)
parks.head(10)["Активность"].plot.pie(ax=area, label="")
# сохранение диаграммы и перевод картинки в кодированный вид
img = BytesIO()
plt.savefig(img)
img = 'data:image/png;base64,' + binascii.b2a_base64(img.getvalue(),
                                                     newline=False).decode("UTF-8")
# настройка вывода количества элементов датафрейма на экран
pd.set_option('display.max_colwidth', 1000)
# создание html документа
html = '''<html>
<head>
    <title>Активности в парках Москвы</title>
    <meta charset="utf-8"/>
</head>
<body>
    <h1>Активности в парках Москвы</h1>
    <img src="''' + img + '''" alt="Популярные парки"/>
    ''' + data.to_html(index=False) + '''
</body>
</html>'''
# настройка pdf документа
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
options = {
    'page-size': 'A4',
    'header-right': '[page]'
}
# перенос html документа  в pdf
pdfkit.from_string(html, 'parks.pdf',
                   configuration=config, options=options)
