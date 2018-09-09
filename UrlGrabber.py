import requests
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from pprint import pprint
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os


url = "https://disneyworld.disney.go.com/dining/"


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
#chrome_driver = webdriver.Chrome("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/local/bin/chromedriver")


#response = requests.get(url)
#html = response.content

driver.get(url)
html = driver.page_source

soup = BeautifulSoup(html)

urls = []
restHtml = open('./restHtml', 'w+')
print >> restHtml, soup
items = soup.findAll('li', attrs={'class': 'card show dining '})
pprint(len(items))
for item in items:
    link = item.find('a', href=True)
    urls.append(link['href'])

pprint(len(urls))
pprint(list(set(urls)))


