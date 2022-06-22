import requests
import json

# get запрос на получение данных геокодера по городу Самара
res = requests.get('https://geocode-maps.yandex.ru/1.x/?geocode=Самара&apikey=43b3ce8e-cbbe-45c5-950d-324d40afc416&format=json&results=1')
# преобразование response объекта в json документ
geo = json.loads(res.content)
# по ступеням добираемся до данных о долготе расположения города Самара, по пути данные изменяются в массив и в конце данные получаются в строковом формате
print(geo['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[0])
