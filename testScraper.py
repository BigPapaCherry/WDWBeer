import requests
from pprint import pprint
from BeautifulSoup import BeautifulSoup
import re

url = 'https://disneyworld.disney.go.com/dining/disney-springs/paddlefish/menus/'
response = requests.get(url)
html = response.content
beerTypes = ['IPA', 'Ale', 'Lager', 'Stout', 'Pilsner', 'Pils', 'Porter', 'Hefeweizen', 'Beer', 'Draft', 'Kolsch', 'Dry', "Imported", "Domestic"]
sep = ','
sep2 = '-'
suffixToBeRemoved = '((\(.*\))|(Beer)|(Draft)|(\d\d-)|(-)|(,)).*'
commaListWithOrRegex = "(([a-zA-Z'\s])*,)*\sor(.*)"

soup = BeautifulSoup(html)

names = []
prices = []
for table in soup.findAll('div', attrs={'class': 'group', 'id': 'Alcoholic Beverage'}):
    title = table.find('h3', attrs={'class': 'group-title'}).text
    for item in table.findAll('div', attrs={'class': 'item'}):
        name = item.find('h4', attrs={'class': 'item-title'}).text
        price = item.findAll('div', attrs={'class': 'price-value'})[1]
        if re.search(commaListWithOrRegex, name):
            pprint('Found List with Or')
            pprint(name)
            listToSep = name.split(",")
            pprint(listToSep)
            lastNames = listToSep[len(listToSep)-1].split(" or ")
            pprint(lastNames)
        elif any(type in title for type in beerTypes) or any(type in name for type in beerTypes):
            name = re.sub(suffixToBeRemoved, '', name).strip()
            names.append(name)


pprint(list(set(names)))

#triples subject, predicate and obect. neo4j is a graph database. semantic database -> look for a beer ontology

#double metaphone. written word for how it sounds. fuzzy matching. check npm
## dbpedia - check for beer names. possbile untappd replacement.
