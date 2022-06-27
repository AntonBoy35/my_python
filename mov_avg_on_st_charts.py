import pandas as pd
import matplotlib.pyplot as plt

# получение данных из удаленного csv файла 
data = pd.read_csv("http://video.ittensive.com/python-advanced/rts-index.csv")
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

data["Date"] = pd.to_datetime(data["Date"], dayfirst=True) # приведение данных с датой к временному типу
dates = pd.date_range(min(data["Date"]), max(data["Date"])) # построение данных по возрастанию дат
data = data.set_index("Date") # назначение даты индексом
data = data.reindex(dates).ffill() # заполнение пустых ячеек с датами предыдущим значением
data["Day"] = pd.to_datetime(data.index).dayofyear # создание столбца с днями года
data.index.name = "Date" # присваивание имени индексу
data = data.sort_index() # сортировка по индексу
data_2019 = data["2019"].reset_index().set_index("Day") # создание фрейма с данными по 2019 году и назначение индексом день года
data_2017 = data["2017"].reset_index().set_index("Day")["Max"].ewm(span=20).mean() # создание фрейма с експонентой максимумов за 20 дней по 2017 году и назначение индексом день года
fig = plt.figure(figsize=(12, 8)) # создание фигуры 12 на 8
area = fig.add_subplot(1, 1, 1) # создание холста
data_2019["Close"].plot(ax=area, color="red", label="2019", lw=3) # отрисовка графика закрытий по 2019 году
data_2017.plot(ax=area, color="orange", label="Exp_2017", lw=3) # отрисовка графика экспонеты по 2017 году
data["2017"].reset_index().set_index("Day")["Close"].plot.area(ax=area, color=".5", label="2017") # отрисовка исходных данных закрытий по 2017 году
data["2018"].reset_index().set_index("Day")["Close"].plot(ax=area, color="blue", label="2018", lw=3) # отрисовка исходных данных закрытий по 2018 году
plt.legend() # подключение легенды
plt.show() # выведение графика на экран
data_fall = data_2019[data_2019["Close"] < data_2017[0:len(data_2019)]] # срез данных по закрытиям в 2019 году если они больше экспоненты 2017 года
data_fall.set_index("Date", inplace=True) # назначение индексом дату
data_fall = data_fall.sort_index(ascending=False) # сортировка по индексу в обратном порядке
print(data_fall.head(1).index) # выведение первого индекса обработанных данных
