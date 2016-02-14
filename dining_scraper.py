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

def find_menu_items(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    items = soup.find_all('p', class_="mini freeze")
    menu = []
    for item in items:
        nicer_item = item.text.strip()
        menu.append(nicer_item)
    return menu