# скользящие средние на биржевых графиках
'''
Используя данные индекса РТС за последние годы
https://video.ittensive.com/python-advanced/rts-index.csv
постройте отдельные графики закрытия (Close) индекса по дням за 2017, 2018, 2019 годы в единой оси X.
Добавьте на график экспоненциальное среднее за 20 дней для значения Max за 2017 год.
Найдите последнюю дату, когда экспоненциальное среднее максимального дневного значения (Max) в 2017 году было больше, чем соответствующее значение Close в 2019 году (это последнее пересечение графика за 2019 год и графика для среднего за 2017 год).
'''
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("http://video.ittensive.com/python-advanced/rts-index.csv")
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

data["Date"] = pd.to_datetime(data["Date"], dayfirst=True) # приводим данные с датой к временному типу и указываем начало с дня
dates = pd.date_range(min(data["Date"]), max(data["Date"])) # выбираем все даты от минимальной до максимальной
data = data.set_index("Date") # назначаем дату индексом
data = data.reindex(dates).ffill() # заполняем пустые даты предыдущим значением
data["Day"] = pd.to_datetime(data.index).dayofyear # создаем столбец с днями года
data.index.name = "Date" # присваиваем имя индексу
data = data.sort_index() # сортируем по индексу
data_2019 = data["2019"].reset_index().set_index("Day") # создаем фрейм с данными по 2019 году и назначаем индексом день года
data_2017 = data["2017"].reset_index().set_index("Day")["Max"].ewm(span=20).mean() # создаем фрейм с експонентой максимумов за 20 дней по 2017 году и назначаем индексом день года
fig = plt.figure(figsize=(12, 8)) # создаем фигуру 12 на 8
area = fig.add_subplot(1, 1, 1) # создаем холст
data_2019["Close"].plot(ax=area, color="red", label="2019", lw=3) # рисуем график закрытий по 2019 году
data_2017.plot(ax=area, color="orange", label="Exp_2017", lw=3) # рисуем график экспонеты по 2017 году
data["2017"].reset_index().set_index("Day")["Close"].plot.area(ax=area, color=".5", label="2017") # рисуем исходные данные закрытий по 2017 году
data["2018"].reset_index().set_index("Day")["Close"].plot(ax=area, color="blue", label="2018", lw=3) # рисуем исходные данные закрытий по 2018 году
plt.legend() # подключаем легенду
plt.show() # выводим графики на экран
data_fall = data_2019[data_2019["Close"] < data_2017[0:len(data_2019)]] # срезаем данные по закрытиям в 2019 году если они больше экспоненты 2017 года
data_fall.set_index("Date", inplace=True) # задаем индексом дату
data_fall = data_fall.sort_index(ascending=False) # сортируем по индексу в обратном порядке
print(data_fall.head(1).index) # выводим первый индекс обработанных данных