import requests
import bs4
import dining_scraper

def scrape_rest():
    url = "http://chicago.menupages.com/restaurants/the-snail/menu"
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    r = requests.get(url, headers=headers)
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    items = soup.find_all('cite')
    menu = []
    for item in items:
        menu.append(item.text)
    return menu