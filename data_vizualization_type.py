import pandas as pd
import matplotlib.pyplot as plt

# получение данных из csv файла в пандас используя разделитель
data = pd.read_csv("http://video.ittensive.com/python-advanced/data-9722-2019-10-14.utf.csv", delimiter=";")
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

# удаление пустых столбцов
data = data.dropna(axis=1)
# удаление лишних слов в названиях районов и округов
data["District"] = data["District"].str.replace("район ", "").astype("category")
data["AdmArea"] = data["AdmArea"].apply(lambda x: x.split(" ")[0]).astype("category")
# выборка данных за 2018-2019 года
data = data.set_index("YEAR").loc["2018-2019"].reset_index()

# построение круговой диаграммы по данным отличников в округах
fig = plt.figure(figsize=(12, 12))
area = fig.add_subplot(1, 2, 1)
area.set_title("ЕГЭ в Москве", fontsize=20)
data_adm = data.set_index("AdmArea")
data_adm["PASSES_OVER_220"].groupby("AdmArea").sum().plot.pie(ax=area, label="")

# построение круговой диаграммы с отображением количества отличников в каждом районе Северо-Западного округа г. Москва
area = fig.add_subplot(1, 2, 2)
area.set_title("ЕГЭ в СЗАО", fontsize=20)
data_district = data_adm.loc["Северо-Западный"].reset_index().set_index("District")
data_district = data_district["PASSES_OVER_220"].groupby("District").sum()
total = sum(data_district)
data_district.plot.pie(ax=area, label="", autopct=lambda x: int(round(total * x/100))) # округление данных для получения точного значения
plt.show() # вывод всех графических объектов на экран
