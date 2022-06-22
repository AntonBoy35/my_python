import pandas as pd

# Считывание данных о безработице из csv файла
data1 = pd.read_csv("http://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv", delimiter=';')
data1 = data1.set_index(['Year', 'Period']) # установка индексов
# Считывание данных о вызовах пожарных из csv файла
data2 = pd.read_csv("http://video.ittensive.com/python-advanced/data-5283-2019-10-04.utf.csv", delimiter=';')
data2 = data2.set_index(['AdmArea', 'Year', 'Month'])# установка индексов
data2 = data2.loc['Центральный административный округ'] # выборка данных по округу
data2.index.names = ['Year', 'Period'] # переименование первых двух столбцов
data = pd.merge(data1, data2, left_index=True, right_index=True) # слияние фреймов по индексам
data = data.reset_index() # сброс индексов
data = data.set_index('Calls') # переустановка индекса на столбец Call
data = data.sort_index() # сортировка индекса по возрастанию
print(data['UnemployedMen'][0:1]) # вывод среза данных (первой строки) из нужного столбца
