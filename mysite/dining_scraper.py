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
    '''
    Makes an appropriate url given the desired dining hall and meal
    Inputs:
        hall: either "South" or "Bartlett"
        meal: either "Breakfast", "Lunch", "Dinner", or "Brunch"
    Output:
        a url string that links to the appropriate menu
    '''

    halls = {"South": 1604, "Bartlett": 1630}
    meals = {"Breakfast": 296, "Lunch": 297, "Dinner": 298, "Brunch": 1881}
    url = "http://univofchicago.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId={loc}&PeriodId={time}".format(loc = halls[hall], time = meals[meal])
    return url

def get_webpage(url, encoder):
    '''
    Fetches a webpage and reads it into BeautifulSoup
    Inputs:
        url: the url of the site that is being fetched
        encoder: specifies the encoder needed (utf-8 for dining hall site)
    Output:
        soup: a BeautifulSoup of the page
    '''

    # header allows output to match Firefox's seen source code for site (https://developer.mozilla.org/en-US/docs/Web/HTTP/Gecko_user_agent_string_reference)
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    r = requests.get(url, headers=headers)
    r.encoding = encoder
    page = r.text
    # webpage is in html5
    soup = bs4.BeautifulSoup(page, "html5lib")
    return soup

def find_dining_menu_items(hall, meal):
    '''
    Given a hall and meal, returns a list of all menu items available
    Inputs:
        hall: either "South" or "Bartlett"
        meal: either "Breakfast", "Lunch", "Dinner", or "Brunch"
    Output:
        menu: a list of items on the menu at the dining hall for the meal (list of strings)
    '''
    url = make_url(hall, meal)
    soup = get_webpage(url, "utf-8")
    items = soup.find_all('div', class_="menu-name")
    menu = []
    for item in items:
        nicer_item = item.text.strip()
        menu.append(nicer_item)
    return menu

def search_menu(menu, search_item):
    '''
    Searches a list for a search term and returns a list of items that
    match the search term
    This function works for any menu, not just dining hall menus
    Inputs:
        menu: a list of menu items (list of strings)
        search_item: the search term (a string usually input by the user)
    Output:
        return_list: a list of items that match the search (list of strings)
    '''
    return_list = []
    for item in menu:
        # search is case insensitive
        lc_item = item.lower()
        lc_search = search_item.lower()

        if lc_search in lc_item:
            # items only appear once even if there are duplicates in the menu
            if item not in return_list:
                return_list.append(item)

    return return_list