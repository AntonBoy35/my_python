# Парсинг интернет магазина

'''Используя парсинг данных с маркетплейса beru.ru, найдите, на сколько литров отличается общий объем холодильников Саратов 263 и Саратов 452?

Для парсинга можно использовать зеркало страницы beru.ru с результатами для холодильников Саратов по адресу:

video.ittensive.com/data/018-python-advanced/beru.ru/'''

# использовал данные с сайта Ситилинк, т.к. остальные сайты заблокировали бот
import requests
from bs4 import BeautifulSoup
# получаем ссылки на страницы со всеми холодильниками Саратов
header = {'User-Agent': 'ittensive-python-scraper/1.0 (+https://ittensive.com)'} # информация для разработчиков объекта парсинга
url = 'https://www.citilink.ru/catalog/holodilniki/SARATOV/'
r = requests.get(url, headers=header)
html = BeautifulSoup(r.content, features="lxml")
links = html.find_all("a", {'class': 'ProductCardVertical__name Link js--Link Link_type_default'})
# из всех ссылок выбираем только те, которые есть в условии задачи
link_263 = []
link_452 = []
for link in links:
    if str(link).find('Саратов 263') > -1:
        link_263 = link['href']
    if str(link).find('Саратов 452') > -1:
        link_452 = link['href']
# функция выбирающая данные с общим объемом холодильной камеры
def find_volume(link):
    r = requests.get('https://www.citilink.ru' + link)
    html = BeautifulSoup(r.content, features='lxml')
    volume = html.find_all('div', {'class': 'Specifications__column Specifications__column_value'})
    volume = volume[1].get_text()
    volume = volume.split(";")
    return int(''.join(i for i in volume[0] if i.isdigit()))
# проверяем наличие ссылок в списках, если они есть, применяем созданную функцию и получаем объемы
if link_263 and link_452:
    volume_263 = find_volume(link_263)
    volume_452 = find_volume(link_452)
    diff = max(volume_263, volume_452) - min(volume_263, volume_452) # вычисляем разницу объемов
# обработка окончания текстовой фразы для вывода
end = ''
if (diff % 10) == 0 or (diff % 10) > 4:
    end = 'ов.'
elif (diff % 10) == 1:
    end = '.'
else: end = 'а.'
print('Разница в общем объеме холодильных камер холодильников Саратов 263 и Сратов 452 составляет ' +str(diff) +' литр' +end)