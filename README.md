# my_python

# [Сборка ПДФ](https://github.com/AntonBoy35/my_python/blob/main/assembly_PDF.py)

Программа загружает данные из json документа о посещаемости библиотек в различных районах г. Москва, строит круговую диаграмму с информацией о посещаемости в 20ти районах с наиболее популярными библиотеками и создает отчет в pdf формате, состоящий из двух страниц, на первой располагается титульный лист загруженный с сайта, на второй располагается итоговая диаграмма с посещаемостью библиотек, районом с самой большой посещаемостью библиотек и числом посетителей в нем.

# [Автоматический отчет](https://github.com/AntonBoy35/my_python/blob/main/automatic_report.py)

Программа создает отчет полученный из csv файла, содержащий общее число учеников школ г. Москва, набравших более 220 баллов по результатам ЕГЭ, распределение таких учеников по округам, в виде круговой диаграммы. Pdf документ формируется из html кода, изображение с диаграммой передается в html код в data:URI формате (в base64-кодировке). Полученный отчет автоматически отправляется на потовый ящик, html страница полностью отображается в сообщении и дополнительно прикрепляется вложение с таким же отчетом в pdf формате.

# [Объекты культурного наследия](https://github.com/AntonBoy35/my_python/blob/main/cultural_heritage_sites.py)

Программа рисует картограмму регионов РФ, по геоданным из json файла с координатами, выводит на картограмму количество объектов культурного наследия для каждого региона РФ, производит расчет числа объектов культурного наследия в республике Татарстан.

# [Тип визуализации данных](https://github.com/AntonBoy35/my_python/blob/main/data_vizualization_type.py)

Программа выполняет построение двух круговых диаграмм на одной области. На первой диаграмме отображается количество учеников школ г. Москва, набравших 220 и более баллов по результатам ЕГЭ, распределенных по административным округам мест расположения школ обучающихся. На второй диаграмме отображается количество учеников школ г. Москва, набравших 220 и более баллов по результатам ЕГЭ, распределенных по районам Северо-Западного административного округа. Данные загружаются по ссылке из csv файла.
