import pandas as pd

# загружаем данные из csv файла
data = pd.read_csv('http://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv', delimiter=';', index_col='Year')
# создание нового столбца данных по безцаботице людей с органиченными способностями в процентах от всех безработных
data['percent'] = (data['UnemployedDisabled'] * 100) / data['UnemployedTotal']
# отфильтровка данных процент которых меньше двух
data = data[data['percent'] < 2]
# сортировка по индексу
data = data.sort_index()
# вывод среза с результатом на экран
print(data.index[0:1])
