import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

# загрузка данных из csv файла
data = pd.read_csv('http://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv', delimiter=';')
# создание нового столбца с данными по безцаботице людей с органиченными способностями в процентах от всех безработных
data['percent'] = (data['UnemployedDisabled'] * 100) / data['UnemployedTotal']
# группировка данных по году и отфильтровка групп в которых строк меньше 6
data_group = data.groupby('Year').filter(lambda x: x['percent'].count() > 5)
# группировка отфильтрованных данных по году и нахождение среднего значения
data_group = data_group.groupby('Year').mean()
# создание массива данных с индексами группированных данных и изменение структуры массива для работы с sklearn
x = np.array(data_group.index).reshape(len(data_group.index), 1)
# создание массива с данными о среднем проценте людей с органиченными способностями
y = np.array(data_group['percent']).reshape(len(data_group.index), 1)
# создание модели линейной регрессии
model = LinearRegression()
# загрузка в модель данных
model.fit(x, y)
# вывод предсказанного значения процента людей с органиченными способностями в 2020 году, изменение структуры массива и вывод на экран в округленном до двух знаков виде
print(np.round(model.predict(np.array(2020).reshape(1, 1)), 2))
