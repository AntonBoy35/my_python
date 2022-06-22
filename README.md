# my_python

# [Сборка ПДФ](https://github.com/AntonBoy35/my_python/blob/main/assembly_PDF.py)

Программа загружает данные из json документа о посещаемости библиотек в различных районах г. Москва, строит круговую диаграмму с информацией о посещаемости в 20ти районах с наиболее популярными библиотеками и создает отчет в pdf формате, состоящий из двух страниц, на первой располагается титульный лист загруженный с сайта, на второй располагается итоговая диаграмма с посещаемостью библиотек, районом с самой большой посещаемостью библиотек и числом посетителей в нем.

# [Автоматический отчет](https://github.com/AntonBoy35/my_python/blob/main/automatic_report.py)

Программа создает отчет полученный из csv файла, содержащий общее число учеников школ г. Москва, набравших более 220 баллов по результатам ЕГЭ, распределение таких учеников по округам, в виде круговой диаграммы. Pdf документ формируется из html кода, изображение с диаграммой передается в html код в data:URI формате (в base64-кодировке). Полученный отчет автоматически отправляется на потовый ящик, html страница полностью отображается в сообщении и дополнительно прикрепляется вложение с таким же отчетом в pdf формате.

# [Объекты культурного наследия](https://github.com/AntonBoy35/my_python/blob/main/cultural_heritage_sites.py)

Программа рисует картограмму регионов РФ, по геоданным из json файла с координатами, выводит на картограмму количество объектов культурного наследия для каждого региона РФ, производит расчет числа объектов культурного наследия в республике Татарстан.

# [Визуализация данных](https://github.com/AntonBoy35/my_python/blob/main/data_vizualization_type.py)

Программа выполняет построение двух круговых диаграмм на одной области. На первой диаграмме отображается количество учеников школ г. Москва, набравших 220 и более баллов по результатам ЕГЭ, распределенных по административным округам мест расположения школ обучающихся. На второй диаграмме отображается количество учеников школ г. Москва, набравших 220 и более баллов по результатам ЕГЭ, распределенных по районам Северо-Западного административного округа. Данные загружаются по ссылке из csv файла.

# [Фильтрация и изменение данных](https://github.com/AntonBoy35/my_python/blob/main/filtering_and_modifying_data.py)

Программа находит год, с которого процент безработицы среди людей с ограниченными способностями среди всех безработных г. Москва стал менее 2. Данные загружаются с внешнего csv файла и обрабатываются при помощи модуля pandas.

# [Геральдические символы Москвы](https://github.com/AntonBoy35/my_python/blob/main/geraldic.py)

Программа собирает данные о флагах и гербах районов г. Москва и создает pdf отчет с собранными данными. Отчет содержит названия флагов и гербов районов г. Москва, его изображение и описание, все страницы пронумерованы. Данные с описанием геральдических символов и ссылками на изображения загружаются из внешнего источника в csv формате, изображения загружаются из внешнего источника с использованием кода ссылки.

# [Получение данных по API](https://github.com/AntonBoy35/my_python/blob/main/getting_data_via_API.py)

Программа обращается к Яндекс геокодеру, получает информацию об объектах РФ, преобразовывает данные в json формат и выводит данные о долготе г. Самара.

# [Получение котировок акций со страницы сайта](https://github.com/AntonBoy35/my_python/blob/main/getting_quotes.py)

Программа получает данные о котировках акций со страницы (https://mfd.ru/marketdata/?id=5&group=16&mode=3&sortHeader=name&sortOrder=1&selectedDate=01.11.2019) и находит, по какому тикеру был максимальный рост числа сделок (в процентах) за 1 ноября 2019 года.

# [Индексы и объединение фреймов](https://github.com/AntonBoy35/my_python/blob/main/indexes_and_frame_union.py)

Программа получает данные из двух разных внешних источников в csv формате о безработице и вызовах пожарных в г. Москва. Объединяет данные по датам и выводит информацию о безработице среди мужского населения в том месяце, когда было меньше всего вызовоз пожарных в Центральном административном округе.

