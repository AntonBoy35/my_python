# предсказание на 2020 год
'''
Возьмите данные по безработице в городе Москва:
video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv
Сгруппируйте данные по годам, и, если в году меньше 6 значений, отбросьте эти годы.
Постройте модель линейной регрессии по годам среднего значения отношения UnemployedDisabled к UnemployedTotal (процента людей с ограниченными возможностями) за месяц и ответьте, какое ожидается значение процента безработных инвалидов в 2020 году при сохранении текущей политики города Москвы?
Ответ округлите до сотых. Например, 2,32
'''
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

# загружаем данные из csv файла
data = pd.read_csv('http://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv', delimiter=';')
# создаем новый столбец с данными по безцаботице людей с органиченными способностями в процентах от всех безработных
data['percent'] = (data['UnemployedDisabled'] * 100) / data['UnemployedTotal']
# группируем данные по году и отфильтровываем группы в которых строк меньше 6
data_group = data.groupby('Year').filter(lambda x: x['percent'].count() > 5)
# группируем отфильтрованные данные по году и находим среднее значение
data_group = data_group.groupby('Year').mean()
# создаем массив данных с индексами группированных данных и меняем структуру массива для работы со sklearn
x = np.array(data_group.index).reshape(len(data_group.index), 1)
# аналогично создаем массив с данными о среднем проценте людей с органиченными способностями
y = np.array(data_group['percent']).reshape(len(data_group.index), 1)
# создаем модель линейной регрессии
model = LinearRegression()
# подгружаем в модель данные
model.fit(x, y)
# выводим предсказанное значение процента людей с органиченными способностями в 2020 году, меняем структуру массива и
# выводим на экран в округленном до двух знаков виде
print(np.round(model.predict(np.array(2020).reshape(1, 1)), 2))