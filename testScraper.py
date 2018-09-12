import requests
from pprint import pprint
from bs4 import BeautifulSoup
import re

default_url = 'https://disneyworld.disney.go.com/dining/disney-springs/paddlefish/menus/'
variable_url = 'https://disneyworld.disney.go.com/dining/dolphin-hotel/cabana-bar-and-beach-club/menus/'

beerTypes = ['IPA', 'Ale', 'Lager', 'Stout', 'Pilsner', 'Pils', 'Porter', 'Hefeweizen', 'Beer', 'Draft', 'Kolsch', 'Dry', "Imported", "Domestic", "Birra", "Blond"]
sep = ','
sep2 = '-'
suffixToBeRemoved = '((\(.*\))|(Beer)|(Draft)|(\d\d-)|(-)|(,)).*'
commaListWithOrRegex = "(([a-zA-Z'\s])*,)*\sor(.*)"
nonBeerTypes = ['Seasonal', 'Flight', 'Assorted', 'Ask', 'Bottled Beer', 'Canned Beer', 'Draft Beer', 'Woodbridge',
                'Sangria', 'Wine', 'Margarita', 'Premium and Craft', 'Domestic Beer', 'Craft Beer Bucket',
                'Pinot', 'Rosé', 'Root Beer Float', 'Domestic and Craft', 'Cabernet',
                'Imported Beer', 'Premium Beer', 'Draft Beers', 'Bottled Beers', 'Merlot', 'Chardonnay',
                'Specialty Tap Rotation' ]


def store_beer_names( url ):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")

    names = []
    prices = []
    for table in soup.findAll('div', attrs={'class': 'group', 'id': 'Alcoholic Beverage'}):
        title = table.find('h3', attrs={'class': 'group-title'}).text
        for item in table.findAll('div', attrs={'class': 'item'}):
            name = item.find('h4', attrs={'class': 'item-title'}).text
            # price = item.findAll('div', attrs={'class': 'price-value'})[1]
            # if re.search(commaListWithOrRegex, name):
            #     pprint('Found List with Or')
            #     pprint(name)
            #     listToSep = name.split(",")
            #     pprint(listToSep)
            #     lastNames = listToSep[len(listToSep)-1].split(" or ")
            #     pprint(lastNames)
            # el
            if (any(type in title for type in beerTypes) or any(type in name for type in beerTypes)) and not any(type in name for type in nonBeerTypes):
                # if not any(type in name for type in nonBeerTypes):
                    # name = re.sub(suffixToBeRemoved, '', name).strip()
                names.append(name.strip(' \t\n\r'))
    pprint(list(set(names)))
    return names




if __name__ == "__main__":
    store_beer_names(variable_url)

#triples subject, predicate and obect. neo4j is a graph database. semantic database -> look for a beer ontology

#double metaphone. written word for how it sounds. fuzzy matching. check npm
## dbpedia - check for beer names. possbile untappd replacement.
