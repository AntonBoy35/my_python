# Задание: геральдические символы Москвы
'''
Сгенерируйте PDF документ из списка флагов и гербов районов Москвы:
https://video.ittensive.com/python-advanced/data-102743-2019-11-13.utf.csv
На каждой странице документа выведите название геральдического символа (Name), его описание (Description) и его изображение (Picture).
Для показа изображений используйте адрес
https://op.mos.ru/MEDIA/showFile?id=XXX
где XXX - это значение поля Picture в наборе данных. Например:
https://op.mos.ru/MEDIA/showFile?id=8466da35-6801-41a9-a71e-04b60408accb
В случае возникновения проблем с загрузкой изображений с op.mos.ru можно добавить в код настройку для форсирования использования дополнительных видов шифрования в протоколе SSL/TLS.
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
'''
import pandas as pd
import pdfkit
# загрузка данных из csv файла
data = pd.read_csv("http://video.ittensive.com/python-advanced/data-102743-2019-11-13.utf.csv", delimiter=";")
# Создание html документа
html = '''<html>
<head>
    <title>Геральдические символы Москвы</title>
    <meta charset="utf-8"/>
</head>
<body>'''
for i, item in data.iterrows():
    if i == 0:
        html += '<h1>' + item['Name'] + '</h1>'
    else:
        html += '<h1 style="page-break-before:always">' + item['Name'] + '</h1>'
    html += '''<p>
        <img style="width:80%;margin-left:10%"
        src="https://op.mos.ru/MEDIA/showFile?id=''' + item['Picture'] + '''">
    </p>'''
    html += '<p style="font-size:150%">' + item['Description'] + '</p>'
html += '</body></html>'

# настройка документа
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
options = {
    'page-size': 'A4',
    'header-right': '[page]'
}
# генерация pdf документа из html кода
pdfkit.from_string(html, 'heraldic.pdf', configuration=config, options=options)