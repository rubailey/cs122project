'''
This code is all original
Contains code for scraping menupages for menus and csv creation
'''

import requests
import bs4
import dining_scraper
import re
import sqlite3

def scrape_rest(rest_dict, addr):
    '''
    Takes a dictionary of restaurants with attached menupages urls and the address of
    a restaurant and gets the menu for that restaurant.
    Usually returns a list of all menu items and categories together in one list.
    This function is called for every menu request
    Inputs:
        rest_dict: a dictionary; keys are addresses (strings) and values are a tuple where item 0
            is the end of a url in the form /.../ and item 1 is the restaurant's name (string)
        addr: the address of the restaurant whose menu is desired
    Output:
        menu: a list of menu items and headers (all as strings, not differentiated)
        If there is no data in menupages for the restaurant (either no result for the address or
            a blank menu), function returns the string "No Menu Information Available"
    '''


    # if no menupages entry for restaurant
    if not addr in rest_dict:
        return "No Menu Information Available"
    
    url = "http://chicago.menupages.com{link}menu".format(link = rest_dict[addr][0])
    # header allows output to match Firefox's seen source code for site (https://developer.mozilla.org/en-US/docs/Web/HTTP/Gecko_user_agent_string_reference)
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    r = requests.get(url, headers=headers)
    page = r.text
    # webpage is in html5
    soup = bs4.BeautifulSoup(page, "html5lib")
    
    # all menu items
    m_items = soup.find_all('cite')
    # all menu headers
    h_items = soup.find_all('h3')
    
    menu = []
    for item in m_items:
        menu.append(item.text)
    # removes "Now serving" h3 text at top of all menupages pages (not a menu item)
    for item in h_items[1:]:
        menu.append(item.text)
    # if a blank menu on menupages
    if menu == []:
        return "No Menu Information Available"
    
    return menu

def find_rest_list():
    '''
    Pulls a list of all restaurants in the neighborhood from menupages list.
    Returns nothing, but writes the resulting concatenated string of name, link,
    and address to a csv to be turned into a dictionary later by models.py

    This function needs to only be run once on the backend to set up the csv, it is
    never called by the user (time-saving, since the list is assumed constant barring
    change of restaurants, no need to call it every time).
    '''

    # this url is the location of menupages's list of restaurants (neighborhood could be changed if needed)
    url = "http://chicago.menupages.com/restaurants/all-areas/hyde-park-kenwood/all-cuisines/"
    # header allows output to match Firefox's seen source code for site (https://developer.mozilla.org/en-US/docs/Web/HTTP/Gecko_user_agent_string_reference)
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    r = requests.get(url, headers=headers)
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    
    # all list results are in a td entry of this class
    items = soup.find_all('td', class_='name-address')
    
    rest_list = []
    for item in items:
        # name of restaurant is in hyperlink to site, so looking for the 'a' tag will get it
        name = item.find('a').text
        link = item.find('a').get('href')
        # all addresses in HP start with 3 digits and in this form end with |, so re used to find it
        # there is no unique class for the address, it is embedded in text with other extraneous info
        add = re.search('\d\d\d.+\|', str(item.text))
        if add:
            # removes the ' |' that ends all addresses in menupages
            add = add.group()[:-2]

        # concatenates results into one string for insertion into csv
        rest_list.append(str(add) + ", " + str(name) + ", " + str(link))

    # writes strings 
    with open("restaurant_menus.csv", "w") as f:
        for line in rest_list:
            f.write(line + "\n")

'''
As an illustrative example, here is a sample item:
<td class="name-address" scope="row"> <a class="link search_result_link" data-clickstream="" 
data-cs-fires-on-click-link="clicked_searchresults" data-cs-with-property-text='masterlistid: "349901"' 
href="/restaurants/original-pancake-house-2/">Original Pancake House</a> 
Diner, Crepes<br/> 1358 E 47th St | At S Lake Park Ave  </td>

The restaurant name is the text of the 'a' tag, the url is the href attribute of 'a',
and the address is embedded in the text of 'td', but has a standard format and ends with '|'
'''
    

def make_food_truck_csv():
    '''
    Makes csv file from manual search of food truck urls. Never called by user, only needs
    to be run once on backend.
    '''
    
    food_truck_URLs = {"Bob Cha Food Truck":"/restaurants/bob-cha/", 
    "Pierogi Wagon":"/restaurants/pierogi-wagon/", 
    "Ginos Steaks Truck":"restaurants/ginos-steaks-truck/", 
    "The Fat Shallot": "/restaurants/the-fat-shallot/", 
    "Döner Men":"/restaurants/donermen/", 
    "Wao Bao":"/restaurants/wow-bao-5/", 
    "Caponies Express":"/restaurants/caponies-express-2/",
    "The Roost Food Truck": "/restaurants/the-roost/", 
    "The Cheesie's Truck": "/restaurants/cheesies-truck/", 
    "Naansense": "/restaurants/naansense-2/", "Yum Dum Truck": "/restaurants/yum-dum-truck/", "La Cocinita":"/restaurants/la-cocinita/"}

    with open("food_truck_menus.csv","w") as f:
        for key in food_truck_URLs:
            f.write(key + ", " + food_truck_URLs[key] + "\n")

