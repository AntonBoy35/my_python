# numpy и pandas
'''
Возьмите данные по вызовам пожарных служб в Москве за 2015-2019 годы:
https://video.ittensive.com/python-advanced/data-5283-2019-10-04.utf.csv
Получите из них фрейм данных (таблицу значений). По этому фрейму вычислите среднее значение вызовов пожарных машин в месяц в одном округе Москвы, округлив до целых
Примечание: найдите среднее значение вызовов, без учета года
'''

import pandas as pd

# загрузка данных о вызовах пожарных в Московских округах из csv файла
data = pd.read_csv('http://video.ittensive.com/python-advanced/data-5283-2019-10-04.utf.csv', delimiter=';')
print(int(data['Calls'].mean().round())) # выбираем данные из столбца Calls находим среднее значение, округляем до целого и выводим
