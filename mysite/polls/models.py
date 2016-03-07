from django import forms


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

    if 'Food_trucks' in search_params:
        for option in find_food_trucks(cuisine):
            options.append(option)

    if 'Dining_hall' in search_params:
        for 

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
    # take this out
    return None
    ### call yelp thing
