from django import forms
import sqlite3
import sys
sys.path.insert(0, '/home/student/cs122project')
import yelpapi

def Food_search(search_params):
    '''
    takes a dictionary of search parameters and returns a list of food_option objects
    '''
    options = []
    address = '1100 E 57th St, Chicago, IL'
    if 'Address' in search_params:
        address = search_params['Address'] + ', Chicago, IL'

    cuisine = None
    if 'Cuisine' in search_params:
        cuisine = search_params['Cuisine']

    menu_item = None
    if 'Menu_item' in search_params:
        menu_item = search_params['Menu_item']

    if 'Restaurants' in search_params:
        for option in find_restaurants(address, cuisine):
            options.append(option)

    #if 'Food_trucks' in search_params:
    #    for option in find_restaurants(address, cuisine, type='f'):
    #        options.append(option)

    if 'Dining_hall' in search_params:
        for option in []:
            break

    return [food_option(search_params).params]

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

def find_restaurants(address, cuisine):
    '''
    Takes parameters and searches for restaurants matching the search criteria.
    Returns a list of food_option objects.
    '''

    yelpapi.yelp_search(address, term=cuisine)
    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    r = db.execute('SELECT yelp_results.address, healthfails.Risk FROM yelp_results LEFT OUTER JOIN healthfails ON yelp_results.address=healthfails."Address" COLLATE NOCASE;')
    return r.fetchall()
