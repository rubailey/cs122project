import requests
import bs4
import dining_scraper
import re

def scrape_rest(rest_dict, rest):

    url = "http://chicago.menupages.com{link}menu".format(link = rest_dict[rest][1])
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    r = requests.get(url, headers=headers)
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    items = soup.find_all('cite')
    menu = []
    for item in items:
        menu.append(item.text)
    return menu

def find_rest_list():
    url = "http://chicago.menupages.com/restaurants/all-areas/hyde-park-kenwood/all-cuisines/"
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    r = requests.get(url, headers=headers)
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    items = soup.find_all('td', class_='name-address')
    rest_dict = {}
    for item in items:
        name = item.find('a').text
        link = item.find('a').get('href')
        add = re.search('\d\d\d.+\|', str(item.text))
        if add:
            add = add.group()[:-2]
        rest_dict[add] = (name, link)
    return rest_dict

def tester(soup):
    items = soup.find_all('td', class_='name-address')
    print(items[0].find('a').text)
    print(items[0].find('a').get('href'))
    add = re.search('\d\d\d.+\|', str(items[0].text))
    print(add.group()[:-2])

