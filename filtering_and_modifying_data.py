# фильтрация и изменение данных
'''
Получите данные по безработице в Москве:
https://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv
Найдите, с какого года процент людей с ограниченными возможностями (UnemployedDisabled) среди всех безработных (UnemployedTotal) стал меньше 2%.
'''
import pandas as pd
# загружаем данные из csv файла
data = pd.read_csv('http://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv', delimiter=';', index_col='Year')
# создаем новый столбец с данными по безцаботице людей с органиченными способностями в процентах от всех безработных
data['percent'] = (data['UnemployedDisabled'] * 100) / data['UnemployedTotal']
# выбираем данные процент которых меньше двух
data = data[data['percent'] < 2]
# сортируем по индексу
data = data.sort_index()
# выводи срез с результатом на экран
print(data.index[0:1])