import requests
import bs4
import dining_scraper
import re

def scrape_rest(rest_dict, addr):
    '''
    Finds a restaurant's menu given its url and address
    '''
    url = "http://chicago.menupages.com{link}menu".format(link = rest_dict[addr][1])
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
    '''
    Pulls a list of all restaurants in the neighborhood.
    Returns a dictionary: keys are addresses of restaurants and values are
    a tuple of restaurant name and url.
    '''
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

