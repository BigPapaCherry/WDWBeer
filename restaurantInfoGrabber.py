import requests
from pprint import pprint
from bs4 import BeautifulSoup
from neo4j import GraphDatabase, basic_auth
import testScraper

graphenedb_url = "bolt://hobby-ahidnjmgjfpbgbkenhcnlecl.dbs.graphenedb.com:24787"
graphenedb_user = "app134418788-NDHNgQ"
graphenedb_pass = "b.zNNIGYrQPWQc.F0oapaDqPbeLSnwR"

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
# driver = GraphDatabase.driver(graphenedb_url, auth=basic_auth(graphenedb_user, graphenedb_pass))
sess = driver.session()
# To match all nodes except a MasterBeer label (for deletion eventually)
# MATCH (n) where not n:MasterBeer RETURN n LIMIT 775
default_url = 'https://disneyworld.disney.go.com/dining/hollywood-studios/50s-prime-time-cafe/'
variable_url = 'https://disneyworld.disney.go.com/dining/boardwalk/abracadabar/'


def format_menu_url(url):
    menu_url = url + "menus/"

    # pprint("in format url")
    response = requests.get(menu_url, headers={'authority': 'disneyworld.disney.go.com','method': 'GET', 'path': '/dining/boardwalk/abracadabar/', 'scheme': 'https', 'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8','referer': 'https://disneyworld.disney.go.com/dining/boardwalk/abracadabar/', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'x-requested-with': 'XMLHttpRequest'})
    # pprint('after menu lookup')
    menu_html = response.content
    menu_soup = BeautifulSoup(menu_html, features="html.parser")
    urls = []
    for option in menu_soup.findAll('option'):
        if option:
           # pprint(option['value'])
            meal_url = menu_url + option['value']
           # pprint(meal_url)
            urls.append(meal_url)
    # pprint('returning from menu formatter')
    return urls


def grab_restaurant_data(url, rest_name, park, land):
    # pprint('grabbing data for '+url)
    # response = requests.get(url, headers={'authority': 'disneyworld.disney.go.com','method': 'GET', 'path': '/dining/', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'cache-control':'no-cache','pragma': 'no-cache', 'sec-fetch-dest': 'document','sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests':'1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})
    # pprint('response is:')
    # pprint(response)
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
    # names = []
    # pprint('names are')
    # pprint(names)
    if len(names) >0:
        # html = response.content
        # pprint(html)
        # soup = BeautifulSoup(html, features="html.parser")
        # rest_name = soup.find('h1')
        # pprint('rest name is ' + rest_name)
        restParkLoc = park
        # 'fakepark'
        # soup.find('p', attrs={'class': 'locationParkResort location line1'})
        restParkSubLoc = land
        # 'fakesubland'
        # soup.find('p', attrs={'class': 'locationLandArea location line2'})

        if rest_name is not None and restParkLoc is not None:
            if not restParkSubLoc :
                restParkSubLoc = restParkLoc
            # pprint('Land Location is: ' + restParkSubLoc)
            # if restParkSubLoc.text.replace('"', '\\"').strip(' \t\n\r') == 'Walt Disney World® Resort':
            #     restParkSubLoc = restParkLoc
            q = '''MERGE (rest:Restaurant {name:"'''+rest_name+'''"})
            MERGE (park:ParkAreaLoc {name:"''' + restParkLoc + '''"})
            MERGE (park_sub:LandResortLoc {name:"''' + restParkSubLoc + '''"})
            MERGE (park)-[:CONTAINS]->(rest)
            MERGE (park)-[:CONTAINS]->(park_sub)
            MERGE (park_sub)-[:CONTAINS]->(rest)'''
            sess.run(q)
            # pprint('location query ran')

            for beer in names:
                # pprint('processing ' + beer)
                #pprint('adding '+ beer+ ' to graph')
                q = '''MATCH (rest:Restaurant {name:"''' + rest_name+ '''"})
                MERGE (beerName:Beer {name:"''' + beer.replace('"', '\\"') + '''"})
                MERGE (rest)-[:SERVES]->(beerName)'''
                #pprint(q)
                sess.run(q)

           # pprint('Restaurant Name: ' + rest_name.text)
           # pprint('Park/Resort Area: ' + restParkLoc.text)
           # pprint('Park Area/Resort: ' + restParkSubLoc.text)
#    else:
#        pprint("No beers to process url: " + url)


if __name__ == "__main__":
    grab_restaurant_data(default_url)
    # pprint('in main')
    # grab_restaurant_data(variable_url)
