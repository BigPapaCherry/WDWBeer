from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
from selenium.webdriver.chrome.options import Options
import re
import restaurantInfoGrabber
import sys

url = "https://disneyworld.disney.go.com/dining/"
maps_API_key = 'destroyedOldKey,figureouthowtoobfuscatenextkey'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
windows_path = "C:\Program Files (x86)\chromedriver\chromedriver.exe"
mac_path = "/usr/local/bin/chromedriver"


driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=windows_path)


driver.get(url)
html = driver.page_source


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


soup = BeautifulSoup(html, features="html.parser")

urls = []
# restHtml = open('./restHtml', 'w+')
items = soup.findAll('li', attrs={'class': 'card show dining ', 'data-entityid': re.compile('entityType=restaurant$')})
length = len(items)
current = 0
for item in items:
    progress(current, length, '')
    current += 1
    link = item.find('a', href=True)
    #pprint(link)
    if link is not None:
        href = link['href']
        if re.search('disneyworld.disney.go.com', href):
            restaurantInfoGrabber.grab_restaurant_data(href)


