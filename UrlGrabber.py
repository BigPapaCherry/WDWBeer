from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from pprint import pprint
from selenium.webdriver.chrome.options import Options
import re
import restaurantInfoGrabber

url = "https://disneyworld.disney.go.com/dining/"
maps_API_key = 'AIzaSyCigvAncAdGC5Qk17o79XiNdb_eXuhuJh0'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/local/bin/chromedriver")


driver.get(url)
html = driver.page_source

soup = BeautifulSoup(html)

urls = []
restHtml = open('./restHtml', 'w+')
items = soup.findAll('li', attrs={'class': 'card show dining ', 'data-entityid': re.compile('entityType=restaurant$')})
for item in items:
    link = item.find('a', href=True)
    #pprint(link)
    if link is not None:
        href = link['href']
        if re.search('disneyworld.disney.go.com', href):
            restaurantInfoGrabber.grab_restaurant_data(href)


