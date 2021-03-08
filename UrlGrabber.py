from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
from selenium.webdriver.chrome.options import Options
import re
import restaurantInfoGrabber
import sys
import platform
import time
import requests


url = "https://disneyworld.disney.go.com/dining/"
maps_API_key = 'destroyedOldKey,figureouthowtoobfuscatenextkey'
headers = {'authority': 'disneyworld.disney.go.com','method': 'GET', 'path': '/dining/', 'scheme': 'https', 'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8','referer': 'https://disneyworld.disney.go.com/dining/', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'x-requested-with': 'XMLHttpRequest'}

html = requests.get(url, headers=headers)

# requests.get('https://disneyworld.disney.go.com/dining/yacht-club-resort/ale-and-compass-lounge/', headers={'authority': 'disneyworld.disney.go.com','method': 'GET', 'path': '/dining/', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'cache-control':'no-cache','pragma': 'no-cache', 'sec-fetch-dest': 'document','sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests':'1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})
                           # 'referer': 'https://disneyworld.disney.go.com/dining/', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'x-requested-with': 'XMLHttpRequest'})


# how to get untappd search data
# html = requests.get('https://untappd.com/search?q=bud+light&type=beer&sort=all', headers={'authority': 'untappd.com','method': 'GET', 'path': '/search', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'cache-control':'no-cache', 'pragma': 'no-cache', 'referer': 'https://untappd.com/search', 'sec-fetch-dest': 'document','sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests':'1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

soup = BeautifulSoup(html.text, features="html.parser")
# pprint(soup.prettify())
# pprint('after soup')
urls = []
items = soup.findAll('li', attrs={'class': 'card show dining', 'data-entityid': re.compile('entityType=restaurant$')})
# items = ['https://disneyworld.disney.go.com/dining/boardwalk/abracadabar/']
length = len(items)
# pprint(length)
current = 0
for item in items:
    # pprint('inside for loop')
    # pprint(item)
    progress(current, length, '')
    current += 1
    link = item.find('a', href=True)
    rest_name = item.find('h2', attrs={'class': 'cardName'}).text
    # pprint('rest from main page is ' + rest_name)
    location = item.find('span', attrs={'class': 'line1', 'aria-label':'location'}).text.split(',')
    # pprint('location from main page is ')
    # pprint(location[0].strip())
    park = location[0].strip()
    if len(location) > 1 :
        # pprint('2 locations!')
        # pprint(location[1].strip())
        parkLand = location[1].strip()
    else :
        parkLand = park
    # pprint('parkLand is:' +parkLand)
    # link = item
    # pprint(link)
    if link is not None:
        href = link['href']
        # href = item
        if re.search('disneyworld.disney.go.com', href):
            # pprint(href)
            # pprint('  ')
            restaurantInfoGrabber.grab_restaurant_data(href, rest_name, park, parkLand)
# pprint(length)

