from PyPDF2 import PdfFileMerger, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)

# функция для извлечения информации о районе из внутреннего словаря
def extract_district (x):
    return list(map(lambda a: a["District"], x))[0]

# загрузка json документа
r = requests.get("https://video.ittensive.com/python-advanced/data-7361-2019-11-28.utf.json")
# выборка необходимой информации из json документа
data = pd.DataFrame(json.loads(r.content),
                    columns=["NumOfVisitors", "CommonName", "ObjectAddress"]).fillna(value=0)

# извлечение данных о районах Москвы в отдельный столбец
data["District"] = data["ObjectAddress"].apply(extract_district)
# группировка данных по районам и суммирование сгруппированных данных + сортировка по убыванию и срез 20 первых значений
Dist = data.groupby("District").sum().sort_values("NumOfVisitors", ascending=False).reset_index()[0:20]
Dist = Dist.set_index("District") # назначение индекса

# холст
fig = plt.figure(figsize=(9, 5))
area = fig.add_subplot(1, 1, 1)
# вспомогательные данные о сумме всех значений с посещениями
total = sum(Dist["NumOfVisitors"].astype(int))
# круговая диагарамма
Dist.plot.pie(ax=area, cmap="tab20",
              labels=[""]*20, subplots=True, autopct=lambda x: int(total * x/100), fontsize="xx-small")
# легенда для диаграммы
plt.legend(Dist.index,
           bbox_to_anchor=(1, 1, -0.1, -0.1), fontsize="x-small")
# сохранение диаграммы в картинку
plt.savefig("readers.png")

# подготовка ПДФ документа с отчетом о посещаемости библиотек по районам
pdfmetrics.registerFont(TTFont("Trebuchet", "Trebuchet.ttf"))
PDF = canvas.Canvas("readers.pdf", pagesize=pagesizes.A4)
PDF.setFont("Trebuchet", 48)
PDF.drawString(70, 670, "Посетители библиотек")
PDF.drawString(80, 610, "по районам Москвы")
PDF.setFont("Trebuchet", 13)
PDF.drawString(550, 810, "2")
PDF.drawImage(ImageReader("readers.png"), -280, 100)
PDF.setFont("Trebuchet", 20)
PDF.drawString(100, 150, "Самый популярный район")
PDF.setFont("Trebuchet", 24)
PDF.drawString(100, 120, Dist.index[0])
PDF.setFont("Trebuchet", 20)
PDF.drawString(100, 90, "Посетителей: " + str(int(Dist["NumOfVisitors"][0])))
PDF.save()

# объединение двух ПДФ документов в один
merger = PdfFileMerger()
f1 = PdfFileReader(open("title.pdf", "rb"))
f2 = PdfFileReader(open("readers.pdf", "rb"))
merger.append(f1)
merger.append(f2)
merger.write("report.pdf")
