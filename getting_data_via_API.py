# Задание: получение данных по API
'''
Изучите API Геокодера Яндекса
tech.yandex.ru/maps/geocoder/doc/desc/concepts/input_params-docpage/
и получите ключ API для него в кабинете разработчика.
Выполните запрос к API и узнайте долготу точки на карте (Point) для города Самара.
Внимание: активация ключа Геокодера Яндекса может занимать несколько часов (до суток).
В качестве запасного варианта можно использовать этот ключ - 3f355b88-81e9-4bbf-a0a4-eb687fdea256 - он только для выполнения этого задания!
'''
import requests
import json

# get запрос на получение данных геокодера по городу Самара
res = requests.get('https://geocode-maps.yandex.ru/1.x/?geocode=Самара&apikey=43b3ce8e-cbbe-45c5-950d-324d40afc416&format=json&results=1')
# преобразуем данные json формата в контент
geo = json.loads(res.content)
# по ступеням добираемся до данных о долготе расположения города Самара, по пути данные изменяются в массив и в конце данные получаются в строковом формате
print(geo['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[0])