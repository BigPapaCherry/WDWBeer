from BeautifulSoup import BeautifulSoup


url = "https://disneyworld.disney.go.com/dining/"

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)

