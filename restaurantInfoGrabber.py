import requests
from pprint import pprint
from bs4 import BeautifulSoup
from neo4j.v1 import GraphDatabase
import testScraper


uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
sess = driver.session()

default_url = 'https://disneyworld.disney.go.com/dining/hollywood-studios/50s-prime-time-cafe/'
variable_url = 'https://disneyworld.disney.go.com/dining/epcot/food-wine-japanese-hibachi-experience/'


def format_menu_url(url):
    return url + "menus/"


def grab_restaurant_data(url):
    response = requests.get(url)
    # pprint(format_menu_url(url))
    names = testScraper.store_beer_names(format_menu_url(url))
    # pprint(list(set(names)))
    if names:
        html = response.content
        soup = BeautifulSoup(html, features="html.parser")
        rest_name = soup.find('h1')
        restParkLoc = soup.find('p', attrs={'class': 'locationParkResort location line1'})
        restParkSubLoc = soup.find('p', attrs={'class': 'locationLandArea location line2'})
        if rest_name is not None and restParkLoc is not None:
            q = '''MERGE (rest:Restaurant {name:"'''+rest_name.text.replace('"', '\\"')+'''"})
            MERGE (park:ParkAreaLoc {name:"''' + restParkLoc.text.replace('"', '\\"') + '''"})
            MERGE (park_sub:LandResortLoc {name:"''' + restParkSubLoc.text.replace('"', '\\"') + '''"})
            MERGE (park)-[:CONTAINS]->(rest)
            MERGE (park)-[:CONTAINS]->(park_sub)
            MERGE (park_sub)-[:CONTAINS]->(rest)'''
            sess.run(q)
            for beer in names:
                # pprint('processing ' + beer)
                q = '''MATCH (rest:Restaurant {name:"''' + rest_name.text.replace('"', '\\"') + '''"})
                MERGE (beerName:Beer {name:"''' + beer.replace('"', '\\"') + '''"})
                MERGE (rest)-[:SERVES]->(beerName)'''
                # pprint(q)
                sess.run(q)

           # pprint('Restaurant Name: ' + rest_name.text)
           # pprint('Park/Resort Area: ' + restParkLoc.text)
           # pprint('Park Area/Resort: ' + restParkSubLoc.text)
    else:
        pprint("No beers to process url: " + url)


if __name__ == "__main__":
    grab_restaurant_data(default_url)
    grab_restaurant_data(variable_url)
