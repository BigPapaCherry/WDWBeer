import requests
from bs4 import BeautifulSoup
from pprint import pprint
from neo4j import GraphDatabase, basic_auth
import stringMatcher
import re

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
sess = driver.session()

suffixToBeRemoved = '((\(.*\))|(Beer)|(Draft)|(\d\d-)|(-)|(–)|(,)).*'

# headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','authority': 'untappd.com','method': 'GET', 'path': '/search', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'cache-control':'no-cache', 'pragma': 'no-cache', 'referer': 'https://untappd.com/search', 'sec-fetch-dest': 'document','sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests':'1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

def lookupBeerDetails(beerName, current_beer_id) :
    queryBeerName = beerName.replace(' ', '+')
    # pprint(queryBeerName)
    url = 'http://untappd.com/search?q=' + queryBeerName + '&type=beer&sort=all'
    # pprint(url)
    html = requests.get(url, headers=headers)
    # html = requests.get(url)
    # pprint(html.headers)
    # html.encoding='UTF-8'
    # decryptedhtml = brotli.decompress(html.file)
    # pprint(decryptedhtml)
    # pprint(html.ok)
    # pprint(html.content)
    soup = BeautifulSoup(html.text, features="html.parser")
    # pprint(soup.prettify())
    firstBeer = soup.find('div', attrs={'class': 'beer-item'})
    # pprint(firstBeer)
    if firstBeer is not None:
        utBeerName = firstBeer.find('p', attrs={'class': 'name'}).text
        utBreweryName = firstBeer.find('p', attrs={'class': 'brewery'}).text
        ut_style = firstBeer.find('p', attrs={'class': 'style'}).text
        ut_abv = firstBeer.find('p', attrs={'class': 'abv'}).text.strip(' \t\n\r')
        ut_ibu = firstBeer.find('p', attrs={'class': 'ibu'}).text.strip(' \t\n\r')
        # pprint(utBeerName)
        # pprint(utBreweryName)
        # pprint(ut_style)
        # pprint(ut_abv)
        # pprint(ut_ibu)

        q = '''MATCH (beer:Beer) WHERE ID(beer)='''+str(current_beer_id)+'''
                WITH beer
                MERGE (mast:MasterBeer {name:"'''+utBeerName+'''"})
                MERGE (brewery:Brewery {name:"''' + utBreweryName + '''"})
                MERGE (style:BeerStyle {name:"''' + ut_style + '''"})
                MERGE (abv:ABV{name:"''' + ut_abv + '''"})
                MERGE (ibu:IBU{name:"''' + ut_ibu + '''"})
                MERGE (brewery)-[:BREWS]->(mast)
                MERGE (mast)-[:IS_A]->(style)
                MERGE (mast)-[:HAS]->(ibu)
                MERGE (mast)-[:HAS]->(abv)
                MERGE (beer)-[:ALIAS_OF]->(mast)'''
        sess.run(q)

def createAliasRelationship() :
    q = 'match (n:MasterBeer) return n.name as name, ID(n) as id'
    response = sess.run(q)
    nodes = [record for record in response.data()]

    q ='match (n:Beer) return n.name as name, ID(n) as id'
    response = sess.run(q)
    beer_nodes = [record for record in response.data()]
    for beer_node in beer_nodes:


        current_beer = beer_node['name']
        pprint(current_beer)
        current_beer_id = beer_node['id']
        pprint(current_beer_id)



        names = {}
        for node in nodes:
            # pprint(node['name'])
            # pprint(node['id'])
            names[node['id']] = node['name']
        bestMatchID = stringMatcher.checkForBeerMaster(current_beer, names)
        pprint(bestMatchID)

        if bestMatchID is None:
            stripped_beer = re.sub(suffixToBeRemoved, '', current_beer).strip()
            # pprint(stripped_beer)
            lookupBeerDetails(stripped_beer, current_beer_id)
        else:
            pprint('match found')

if __name__ == "__main__":
    createAliasRelationship()
# pprint('in main')
# grab_restaurant_data(variable_url)

# lookupBeerDetails('bud light')
# lookupBeerDetails('coors light')
# lookupBeerDetails('miller light')
# lookupBeerDetails('dogfish head 60 minute')
# lookupBeerDetails('dogfish head 90 minute')
