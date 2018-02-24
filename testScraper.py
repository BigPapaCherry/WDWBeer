import requests
from pprint import pprint
from BeautifulSoup import BeautifulSoup
import re


url = 'https://disneyworld.disney.go.com/dining/hollywood-studios/baseline-tap-house/menus/'
response = requests.get(url)
html = response.content


soup = BeautifulSoup(html)


#table = soup.find('div', attrs={'class':'group', 'id':'Alcoholic Beverage'})

names = []
prices = []
for table in soup.findAll('div', attrs={'class':'group', 'id':'Alcoholic Beverage'}):
	for item in table.findAll('div', attrs={'class':'item'}):
	#    dict = {}
		name = item.find('h4', attrs={'class':'item-title'}).text
		price = item.findAll('div', attrs={'class':'price-value'})[1]
	#    dict['description'] = item.find('div', attrs={'class':'item-description'}).text

	#    dict['price'] = item.find('div', attrs={'class':'price-value'}).text
	#    content.append(dict)
		if not re.search('Flight', name) :   
			names.append(name)
	#        for pri in price:
	#            pprint(pri.text)
			pprint(price.text)

pprint(list(set(names)))  

    