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

def make_url(hall, meal):
    halls = {"South": 1604, "Bartlett": 1630}
    meals = {"Breakfast": 296, "Lunch": 297, "Dinner": 298, "Brunch": 1881}
    url = "http://univofchicago.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId={loc}&PeriodId={time}".format(loc = halls[hall], time = meals[meal])
    return url

def get_webpage(url, encoder):
    r = requests.get(url)
    r.encoding = encoder
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    return soup

def find_dining_menu_items(hall, meal):
    url = make_url(hall, meal)
    soup = get_webpage(url, "utf-8")
    items = soup.find_all('p', class_="mini freeze")
    menu = []
    for item in items:
        nicer_item = item.text.strip()
        menu.append(nicer_item)
    return menu

def search_menu(menu, search_item):
    return_list = []
    for item in menu:
        lc_item = item.lower()
        lc_search = search_item.lower()
        if lc_search in lc_item:
            return_list.append(item)
    return return_list