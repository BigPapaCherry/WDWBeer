import requests
from pprint import pprint
from BeautifulSoup import BeautifulSoup
import re

url = 'https://disneyworld.disney.go.com/dining/hollywood-studios/baseline-tap-house/menus/'
response = requests.get(url)
html = response.content
beerTypes = ['IPA', 'Ale', 'Lager', 'Stout', 'Pilsner', 'Pils', 'Porter', 'Hefeweizen', 'Beer']

soup = BeautifulSoup(html)

names = []
prices = []
for table in soup.findAll('div', attrs={'class': 'group', 'id': 'Alcoholic Beverage'}):
    title = table.find('h3', attrs={'class': 'group-title'}).text
    if any(type in title for type in beerTypes):
        for item in table.findAll('div', attrs={'class': 'item'}):

            name = item.find('h4', attrs={'class': 'item-title'}).text
            pprint('Title Said Beer')
            names.append(name)
    else:
        for item in table.findAll('div', attrs={'class': 'item'}):

            name = item.find('h4', attrs={'class': 'item-title'}).text
            price = item.findAll('div', attrs={'class': 'price-value'})[1]

            if any(type in name for type in beerTypes):
                names.append(name)

pprint(list(set(names)))
