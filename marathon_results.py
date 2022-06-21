# Результаты марафона

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
# функция перевода времени из списка в секунды
def to_sec (time):
    count = 0
    sum_time = 0
    for i in time:
        i = int(i)
        if (count == 0) and (i > 0):
            hour = i * 3600
            count += 1
        elif (count == 0) and (i == 0):
            hour = i
            count += 1
        elif (count == 1) and (i > 0):
            min = i * 60
            count += 1
        elif (count == 1) and (i == 0):
            min = i
            count += 1
        else:
            sec = i
    sum_time = hour + min + sec
    return sum_time

sns.set_context("paper", font_scale=1)
data = pd.read_csv("http://video.ittensive.com/python-advanced/marathon-data.csv", delimiter=",")
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)
data["split"] = data["split"].apply(lambda x: to_sec(x.split(":")))
data["final"] = data["final"].apply(lambda x: to_sec(x.split(":")))

sns.pairplot(data, hue="gender", height=4) # график корреляций, цветовая маркировка по hue="gender"
plt.show()
sns.jointplot("split", "final", data, height=12, kind="kde") # корреляционный график с распределениями
plt.show()
# округленный коэффициент корреляции Пирсона (вывод: имеем право применить линейную регрессию для предсказания)
print (round(stats.pearsonr(data["split"], data["final"])[0], 2))
