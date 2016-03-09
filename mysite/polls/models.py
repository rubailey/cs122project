from django import forms
import sqlite3
import sys
sys.path.insert(0, '/home/student/cs122project/mysite')
import yelpapi
import menu_scraper
from dining_scraper import search_menu

DEFUALT_WALK_TIME = 25
DEFAULT_ADDRESS = '1100 E 57th St, Chicago, IL'
def Food_search(search_params):
    '''
    takes a dictionary of search parameters and returns a list of food_option objects
    '''
    rv = []

    drop()
    
    if search_params['Address'] == None:
        address = DEFAULT_ADDRESS
    else:
        if not 'Chicago' in search_params['Address']:
            address = search_params['Address'] + ', Chicago, IL'

    cuisine = search_params['Cuisine']

    menu_item = search_params['Menu_item']

    walk_time = search_params['walk_time']

    inspection = search_params['inspection']
    if walk_time == None:
        walk_time = DEFUALT_WALK_TIME = 25

    if not menu_item == None:
        if 'Restaurants' in search_params['Types']:
            rest_dict = {}
            with open("polls/restaurant_menus.csv") as f:
                for line in f:
                    add, name, url = line.strip().split(',')
                    url = url.strip()
                    rest_dict[add] = (url, name)
        if 'Food_trucks' in search_params['Types']:
            truck_dict = {}
            with open("polls/food_truck_menus.csv") as f:
                for line in f:
                    name, url = line.strip().split(',')
                    url = url.strip()
                    rest_dict[name] = (url)
        
    if 'Restaurants' in search_params['Types']:
        header, options = find_restaurants(address, cuisine, walk_time, inspection)
        options_r = [header]
        print(options)
        print(type(options))
        for op in options:
            mini_list = []
            for i in range(len(op)):
                print (op[i])
                mini_list.append(op[i])
            if not menu_item == None:
                print("tamogachi")
                menu = menu_scraper.scrape_rest(rest_dict, op[1])
                print("here")
                if type(menu) == str:
                    print("here")
                    mini_list.append(menu)
                else:
                    items = search_menu(menu, menu_item)
                    print("here")
                    if items == []:
                        print("here")
                        items = "No Menu Items Matched"
                    elif len(items) > 5:
                        print("here")
                        items = items[:5]
                    mini_list.append(items)
            options_r.append(mini_list)
        if not menu_item == None:
            options_r[0].append('Menu Items')


        rv.append(options_r)

    #if 'Food_trucks' in search_params:
    #    for option in find_restaurants(address, cuisine, type='f'):
    #        options.append(option)

    if 'Dining_hall' in search_params:
        for option in []:
            break

    return rv

class food_option(object):
    def __init__(self, line):
        '''
        takes in a result from a sqlite3 search and gives a class object where self.result
        is in the form which we want to return
        '''
        # needed?
        self.params = line
        self.address = None
        self.name = None

class SearchForm(forms.Form):
    Cuisine = forms.CharField()
    Menu_item = forms.CharField()
    Address = forms.CharField()

def find_restaurants(address, cuisine, walk_time, inspection, rating=None):
    '''
    Takes parameters and searches for restaurants matching the search criteria.
    Returns a list of food_option objects.
    '''

    yelpapi.yelp_search(address, cuisine)
    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    
    selectline = 'SELECT yelp_results.name, yelp_results.address, yelp_results.rating, yelp_results.phone_number, yelp_results.walking_time'
    header = ['Name', 'Address', 'Rating', 'Phone', 'Walking Time']
    fromline = ' FROM yelp_results'
    whereline = ' WHERE yelp_results.walking_time < ?;'
    if inspection:
        selectline += ', healthfails.Risk'
        header.append('Risk')
        fromline += ' LEFT OUTER JOIN healthfails ON yelp_results.address=healthfails.Address COLLATE NOCASE'

    r = db.execute(selectline + fromline + whereline, [walk_time])
    tuple_list = r.fetchall()
    return (header,tuple_list)

def drop():
    yelpapi.drop_yelp_table("yelp_results")

#def find_food_trucks(address, cuisine):
