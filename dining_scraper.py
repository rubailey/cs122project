'''
URLs: "http://univofchicago.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=XXXX&PeriodId=YYYY"
XXXX:
Bartlett: 1630
South: 1604

YYYY:
Breakfast(M,T,W,R,F): 296
Lunch(M,T,W,R,F): 297
Dinner (U,M,T,W,R,F): 298
Brunch (S,U): 1881
'''

import bs4
import requests

def get_webpage(url, encoder):
    r = requests.get(url)
    r.encoding = encoder
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    return soup

def find_dining_menu_items(url):
    soup = get_webpage(url, "utf-8")
    items = soup.find_all('p', class_="mini freeze")
    menu = []
    for item in items:
        nicer_item = item.text.strip()
        menu.append(nicer_item)
    return menu

def find_menupages_items(url):
    pass