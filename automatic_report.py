import pandas as pd
import matplotlib.pyplot as plt
import pdfkit
from io import BytesIO
import binascii
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# получаем данные из csv файла используя разделитель
data = pd.read_csv("http://video.ittensive.com/python-advanced/data-9722-2019-10-14.utf.csv", delimiter=";")
data = data[data["YEAR"] == "2018-2019"] # фильтруем данные только по 2018-2019 годам
data_best = data.sort_values("PASSES_OVER_220", ascending=False).head(1) # школа с наибольшим количством отличников
data["AdmArea"] = data["AdmArea"].apply(lambda x: x.split(" ")[0]) # фильтр названий округов
data_adm = data.groupby("AdmArea").sum()["PASSES_OVER_220"].sort_values() # группировка округов по отличникам
total = data_adm.sum() # общее количство отличников
# холст
fig = plt.figure(figsize=(11, 6))
area = fig.add_subplot(1, 1, 1)
# вытаскивание сектора из диаграммы
explode = [0]*len(data_adm)
explode[0] = 0.4
explode[1] = 0.4
# отрисовка круговой диаграммы
data_adm.plot.pie(ax=area,
                  labels=[""]*len(data_adm),
                  label="Отличники по ЕГЭ",
                  cmap="tab20",
                  autopct=lambda x: int(round(total * x/100)),
                  pctdistance=0.9,
                  explode=explode)
plt.legend(data_adm.index, bbox_to_anchor=(1.5, 1, 0.1, 0)) # вынос легенды

img = BytesIO() # создание бинарного объекта
plt.savefig(img) # сохранение диаграммы в бинарный объект
# перекодировка фото диаграммы из base64 в utf-8
img = 'data:image/png;base64,' + binascii.b2a_base64(img.getvalue(),
                            newline=False).decode("UTF-8")
pd.set_option("display.max_colwidth", 1000) # устанавливаем ограничение на количество выводимы символов
# верстка html документа
html = '''<html>
<head>
    <title>Результаты ЕГЭ Москвы: отличники</title>
    <meta charset="utf-8"/>
</head>
<body>
    <h1>Результаты ЕГЭ Москвы: отличники в 2018-2019 году</h1>
    <p>Всего: ''' + str(total) + '''</p>
    <img src="''' + img + '''" alt="Отличники по округам"/>
    <p>Лучшая школа: ''' + str(data_best["EDU_NAME"].values[0]) + '''</p>
</body>
</html>'''
# настройка pdf холста
config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
options = {
    'page-size': 'A4',
    'header-right': '[page]'
}
# запись html документа в пдф
pdfkit.from_string(html, 'ege.best.pdf',
                   configuration=config, options=options)

letter = MIMEMultipart() # создание MIME объекта

# добавление информации в MIME объект
letter["From"] = "=?utf-8?b?0JDQvdGC0L7QvSDQkdC+0LnQutC+?= <aboiko35@yandex.ru>"
letter["Subject"] = "Результаты по ЕГЭ в Москве"
letter["Content-Type"] = "text/html; charset=utf-8"
letter["To"] = "support@ittensive.com"
letter.attach(MIMEText(html, "html")) # вывод html документа в письмо
# создание вложения к письму
attachment = MIMEBase("application", "pdf")
attachment.set_payload(open("ege.best.pdf", "rb").read())
attachment.add_header("Content-Disposition",
                      'attachment; filename="ege.best.pdf"')
encoders.encode_base64(attachment)
letter.attach(attachment) # прикрепление вложения к письму
# настройка и отправка письма на сервер используя защищенный smtp протокол
user = "aboiko35@yandex.ru"
password = "XXX"
server = smtplib.SMTP_SSL("smtp.yandex.com", 465)
server.login(user, password)
server.sendmail("aboiko35@yandex.ru",
                "support@ittensive.com",
                letter.as_string())
server.quit() # закрытие соединения с сервером
