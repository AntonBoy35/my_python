import matplotlib.pyplot as plt
import  geopandas as gpd
import pandas as pd
import descartes

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)


data_obj = pd.read_csv("data-44-structure-4.csv.gz", usecols=["Объект", "Регион"]) # данные с объектами культурного наследия из файла
data_obj["Регион"] = data_obj["Регион"].str.upper()# приведение названия регионов в верхнему регистру
data_obj = data_obj.groupby("Регион").count() # группировка данных по регионам и подсчет количества объектов

data_geo = gpd.read_file("russia.json") # данные с координатами границ РФ из файла
data_geo = data_geo.to_crs({"init": "epsg:3857"}) # преобразование проекции к Меркатору
data_geo["NL_NAME_1"] = data_geo["NL_NAME_1"].str.upper() # приведение названия регионов в верхнему регистру
# приведение названий различающихся данных к одному значению
data_geo = data_geo.replace({
    "ХАНТЫ-МАНСИЙСКИЙ АВТОНОМНЫЙ ОКРУГ": "ХАНТЫ-МАНСИЙСКИЙ АВТОНОМНЫЙ ОКРУГ - ЮГРА",
    "РЕСПУБЛИКА АДЫГЕЯ": "РЕСПУБЛИКА АДЫГЕЯ (АДЫГЕЯ)",
    "ЧУВАШСКАЯ РЕСПУБЛИКА": "ЧУВАШСКАЯ РЕСПУБЛИКА - ЧУВАШИЯ",
    "РЕСПУБЛИКА МАРИЙ-ЭЛ": "РЕСПУБЛИКА МАРИЙ ЭЛ",
    "РЕСПУБЛИКА СЕВЕРНАЯ ОСЕТИЯ": "РЕСПУБЛИКА СЕВЕРНАЯ ОСЕТИЯ - АЛАНИЯ",
    "РЕСПУБЛИКА ТАТАРСТАН": "РЕСПУБЛИКА ТАТАРСТАН (ТАТАРСТАН)"
})
# объединение данных
data_geo = pd.merge(left=data_geo,
                    right=data_obj,
                    left_on="NL_NAME_1",
                    right_on="Регион",
                    how="left")
# print(data_geo[data_geo["Объект"].isnull()]) # проверка корректности объединения данных
# холст
fig = plt.figure(figsize=(15, 12))
area = plt.subplot(1, 1, 1)
# картограмма РФ
data_geo.plot(ax=area, legend=True, column="Объект", cmap="Reds")
area.set_xlim(2e6, 2e7) # отрезание крайних областей для увеличения картограммы
# подпись кол-ва объектов в регионах на картограмме
for _,region in data_geo.iterrows():
     area.annotate(region["Объект"],
                   xy=(region.geometry.centroid.x,
                       region.geometry.centroid.y), fontsize=8)
plt.show() # вывод картограммы на экран
data = data_geo[data_geo["NL_NAME_1"] == "РЕСПУБЛИКА ТАТАРСТАН (ТАТАРСТАН)"] # выборка данных по республике Татарстан
print("В республике Татарстан находится " + str(data["Объект"].values[0]) + " объектов культурного наследия.") # кол-во объектов культурного наследия в республике Татарстан
