import requests
from pprint import pprint
from bs4 import BeautifulSoup
from neo4j.v1 import GraphDatabase
import testScraper


uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
sess = driver.session()

default_url = 'https://disneyworld.disney.go.com/dining/hollywood-studios/50s-prime-time-cafe/'
variable_url = 'https://disneyworld.disney.go.com/dining/boardwalk/trattoria-al-forno/'


def format_menu_url(url):
    menu_url = url + "menus/"

  #  pprint("in format url")
    response = requests.get(menu_url)
    menu_html = response.content
    menu_soup = BeautifulSoup(menu_html, features="html.parser")
    urls = []
    for option in menu_soup.findAll('option'):
        if option:
           # pprint(option['value'])
            meal_url = menu_url + option['value']
           # pprint(meal_url)
            urls.append(meal_url)
    return urls


def grab_restaurant_data(url):
    response = requests.get(url)
    # pprint(format_menu_url(url))
    formatted_urls = format_menu_url(url)
    names = []
    for formatted_url in formatted_urls:
        temp_names = testScraper.store_beer_names(formatted_url)
       # pprint(formatted_url)
       # pprint(temp_names)
        names.append(temp_names)
   # pprint(names);
    #names = testScraper.store_beer_names(format_menu_url(url))
    # pprint(list(set(names)))
    names = set([item for sublist in names for item in sublist])
    #pprint(names)
    if names:
        html = response.content
        soup = BeautifulSoup(html, features="html.parser")
        rest_name = soup.find('h1')
        restParkLoc = soup.find('p', attrs={'class': 'locationParkResort location line1'})
        restParkSubLoc = soup.find('p', attrs={'class': 'locationLandArea location line2'})
        if rest_name is not None and restParkLoc is not None:
            q = '''MERGE (rest:Restaurant {name:"'''+rest_name.text.replace('"', '\\"').strip(' \t\n\r')+'''"})
            MERGE (park:ParkAreaLoc {name:"''' + restParkLoc.text.replace('"', '\\"').strip(' \t\n\r') + '''"})
            MERGE (park_sub:LandResortLoc {name:"''' + restParkSubLoc.text.replace('"', '\\"').strip(' \t\n\r') + '''"})
            MERGE (park)-[:CONTAINS]->(rest)
            MERGE (park)-[:CONTAINS]->(park_sub)
            MERGE (park_sub)-[:CONTAINS]->(rest)'''
            sess.run(q)

            for beer in names:
                # pprint('processing ' + beer)
                #pprint('adding '+ beer+ ' to graph')
                q = '''MATCH (rest:Restaurant {name:"''' + rest_name.text.replace('"', '\\"').strip(' \t\n\r') + '''"})
                MERGE (beerName:Beer {name:"''' + beer.replace('"', '\\"').strip(' \t\n\r') + '''"})
                MERGE (rest)-[:SERVES]->(beerName)'''
                #pprint(q)
                sess.run(q)

           # pprint('Restaurant Name: ' + rest_name.text)
           # pprint('Park/Resort Area: ' + restParkLoc.text)
           # pprint('Park Area/Resort: ' + restParkSubLoc.text)
    else:
        pprint("No beers to process url: " + url)


if __name__ == "__main__":
    #grab_restaurant_data(default_url)
    grab_restaurant_data(variable_url)
