'''
Original code, runs the search
'''


from django import forms
import sqlite3
import yelpapi
import menu_scraper
import dining_scraper
import google_dist

DEFAULT_WALK_TIME = 25
# The Reg
DEFAULT_ADDRESS = '1100 E 57th St, Chicago, IL'

def Food_search(search_params):
    '''
    takes a dictionary of search parameters(as described in
    views.py)and returnsa list where each item in the 
    list represents either restaurants, food trucks or 
    dining halls (each only apears if requested).
    Each item in that list(eg the list for restaurants) represents
    a row in the final table. This row is represented by a tuple
    which the first item is a list of items in the row and the second
    is a boolean which is true iff the row is a header. 
    Each item in the row should match up with the collumn name in
    the header. These items are tuples were the first is the information
    which will be shown in the table and the second is a boolean which
    is true only if the information will be shown as a bulleted list
    (which is only true for menu items)

    this code works by handeling each case of restaurant, food trucks
    and dining hall seperatly

    '''
    rv = []

    #takes the search_params dict and turns it into local variables
    if search_params['Address'] == None:
        address = DEFAULT_ADDRESS
    else:
        if not 'Chicago' in search_params['Address']:
            address = search_params['Address'] + ', Chicago, IL'

    cuisine = search_params['Cuisine']

    menu_item = search_params['Menu_item']

    walk_time = search_params['walk_time']

    inspection = search_params['inspection']

    rating = search_params['Rating']


    if walk_time == False:
        walk_time = DEFAULT_WALK_TIME

    #creates dictionarys mapping keys (address for restaurands
    # name for foodtrucks) to a tuple with menupages url
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
                    #creates a tuple of length 1 so it can be handled the same as rest_dict
                    truck_dict[name] = (url,)
        
    #code for restaurants
    if 'Restaurants' in search_params['Types']:

        #calls the code which gets list of restaurants from yelp
        header, options = find_restaurants(address, cuisine, walk_time, inspection, rating)
        
        #initializes local value which will be appended to RV with header
        options_r = [(header, True)]
        
        if options == []:
            options_r.append(("No Restaurants in Hyde Park Matched Your Search",True))
        appended_list = []
        
        #cycles through all options
        for op in options:

            #occasionally options are repeated, filters these out
            if not op[0] in appended_list:
                #initializes the list which will have the row information
                mini_list = []
                for i in range(len(op)):
                    #Boolean is False because none of these are lists
                    mini_list.append((op[i], False))

                #if there is a menu item, calls menupages
                if not menu_item == None:
                    menu = menu_scraper.scrape_rest(rest_dict, op[1])
                    if type(menu) == str:
                        #this will happen only if no menu information
                        mini_list.append(([menu], True))
                    
                    else:
                        items = dining_scraper.search_menu(menu, menu_item)
                        
                        #Checks if items is empty
                        if items == []:
                            items = "No Menu Items Matched"
                            mini_list.append(([items], True))
                        
                        #cuts list off at 5 items
                        elif len(items) > 5:
                            items = items[:5]
                            mini_list.append((items, True))
                        else:
                            mini_list.append((items, True))
                
                #none of these rows are headers, so boolean is False
                options_r.append((mini_list, False))
                appended_list.append(op[0])

        #appends menu items to header if necesary
        if not menu_item == None:
            options_r[0][0].append(('Menu Items', False))


        rv.append(options_r)

    #handles the case for foodtrucks, similar to restaurants code
    if 'Food_trucks' in search_params['Types']:

        #calls code which gets list of foodtrucks from yelp and food truck finder
        header, options = find_food_trucks(address, cuisine, walk_time, rating)
        
        #initializes return value with header
        options_ft = [(header, True)]
        appended_list = []
        
        #loops through options
        for op in options:

            #checks to make sure none of the trucks have already been added
            if not op[0] in appended_list:

                #initializes list which will have row information
                mini_list = []
                for i in range(len(op)):
                    #adds information to row, boolean is false because none of these are tables
                    mini_list.append((op[i], False))
                
                if not menu_item == None:
                    #calls menupages to get menu
                    menu = menu_scraper.scrape_rest(truck_dict, op[0])
                    
                    #will only happen if no menu information was available
                    if type(menu) == str:
                        mini_list.append(([menu], True))
                    
                    else:
                        #finds if menu items matched
                        items = dining_scraper.search_menu(menu, menu_item)
                        if items == []:
                            items = ["No Menu Items Matched"]
                        
                        #cuts off returned items at 5
                        elif len(items) > 5:
                            items = items[:5]
                        mini_list.append((items, True))

                #appends row to table, boolean is false because it is not header
                options_ft.append((mini_list, False))
                appended_list.append(op[0])
        
        #adds menu items to header
        if not menu_item == None:
            options_ft[0][0].append(('Menu Items', False))
        #print (options_ft)
        rv.append(options_ft)

        
    #for dining halls
    if 'Dining_hall' in search_params['Types']:

        #calls code which gets dining halls and menus
        header, options, menus = find_dining_halls(address)
        
        #initializes return table with header
        options_dh = [(header, True)]
        
        #adds menu items to header
        if not menu_item == None:
            header.append(("Menu Items", False))
        
        #loops through options
        for i in range(len(options)):

            #row to be appended to table (one for south, one for bartlet)
            mini_list = []
            for x in range(len(options[i])):
                #boolean is false because none of these items are bulleted lists 
                mini_list.append((options[i][x], False))

            if not menu_item == None:

                #calls code to search menus for menu item
                items = dining_scraper.search_menu(menus[i], menu_item)
                if items == []:
                    #will always be a menu, only empty if no items matched
                    items = ["No Menu Items Matched"]
                
                #limits return list to 5
                elif len(items) > 5:
                    items = items[:5]

                #appends menu items to row
                mini_list.append((items, True))

            #adds row to table
            options_dh.append((mini_list, False))
        rv.append(options_dh)

    return rv



def find_restaurants(address, cuisine, walk_time, inspection, rating=None):
    '''
    Takes parameters and searches for restaurants matching the search criteria.
    Returns a tuple with a header and a list of tuples representing restaurants
    This code uses sqlite3 to search the yelp table and healthfails table
    '''

    #creates the database using yelp_search in yelpapi
    yelpapi.yelp_search(address, cuisine)
    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    header = []

    #creates header in the form of a row in the Food_Search return value
    header_list = ['Restaurants', 'Address', 'Rating', 'Phone', 'Walking Time']
    for i in range(len(header_list)):
        header.append((header_list[i], False))
    
    #sqlite 3 search strings initialization
    selectline = 'SELECT yelp_results.name, yelp_results.address, yelp_results.rating, yelp_results.phone_number, yelp_results.walking_time'
    fromline = ' FROM yelp_results'
    whereline = ' WHERE yelp_results.walking_time < ?'
    
    #adds to sqlite3 search strings as necesary if inspection
    if inspection:
        selectline += ', healthfails.Risk'
        header.append(('Risk', False))
        fromline += ' LEFT OUTER JOIN healthfails ON yelp_results.address=healthfails.Address COLLATE NOCASE'

    #creates end_list (we are always searching for walk_time)
    end_list = [walk_time]

    #appends to lines and end_list as necesary if rating parameter
    if not rating == None:
        whereline += ' and yelp_results.rating >= ?'
        end_list.append(rating)

    #executes the search, drops the table and closes the database
    r = db.execute(selectline + fromline + whereline + ';', end_list)
    tuple_list = r.fetchall()
    yelpapi.drop_yelp_table("yelp_results")
    db.close()

    return (header,tuple_list)

def find_food_trucks(address, cuisine, walking_time, rating = None):
    '''
    Takes parameters and searches for foodtrucks matching the search criteria.
    Returns a tuple with a header and a list of tuples representing restaurants
    This code uses sqlite3 to search the yelp food truck table
    '''
    #calls yelp_search_food_trucks in yelpapi
    yelpapi.yelp_search_food_trucks(address, cuisine)
    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()

    #constructs the header row as required in Food_search
    header = []
    header_list = ['Food Trucks', 'Rating', 'Phone', 'Arrive Time', 'Depart Time']
    for i in range(len(header_list)):
        header.append((header_list[i], False))

    #initializes the sqlite3 search strings
    selectline = 'SELECT yelp_food_trucks.name, yelp_food_trucks.rating, yelp_food_trucks.phone_number, yelp_food_trucks.arrive_time, yelp_food_trucks.leave_time'
    fromline = ' FROM yelp_food_trucks'
    whereline = ' WHERE yelp_food_trucks.walking_time < ?'
    
    #initializes end_list
    end_list = [walking_time]

    #handles the case of searching for a specific rating
    if not rating == None:
        whereline += ' and yelp_food_trucks.rating >= ?'
        end_list.append(rating)

    #does the sqlite3 search and returns, closes the database and drops the table
    r=db.execute(selectline + fromline + whereline + ';', end_list)
    tuple_list = r.fetchall()
    db.close()
    yelpapi.drop_yelp_table("yelp_food_trucks")

    return (header, tuple_list)

def get_dining_hall(hall, address):
    '''
    Finds the lunch or brunch menu for a given hall and calculates walking time
    Inputs:
        hall: a dining hall name, either "Bartlett" or "South"
        address: the provided address of the user
    Output: two items:
        a list containing the name of the Dining Hall, the address, and the 
            walking time
        the menu for that day, a list

    This function is called by find_dining_halls
    '''

    addresses = {"Bartlett": "5640 S University Ave", "South": "6025 S Ellis Ave"}
    menu = dining_scraper.find_dining_menu_items(hall, "Lunch")
    if menu == []:
        # every day has either lunch or brunch
        menu = dining_scraper.find_dining_menu_items(hall, "Brunch")

    # makes sure Google searches in Chicago instead of some random place
    dh_addr = addresses[hall] + ", Chicago"
    dist, time = google_dist.get_distance(address, dh_addr)

    if not 'hour' in time:
        time = int(time.split()[0])
    # makes sure result is in minutes
    else:
        time = 60*int(time.split()[0]) + int(time.split()[2])
    
    return [hall + " Dining Hall", addresses[hall], time], menu


def find_dining_halls(address):
    '''
    with a given address returns a tuple of the header for the table, 
    the list of tuples of dining options and the menus for those dining halls
    '''
    #creates the header of the form required in Food_search
    header = []
    header_list = ['Dining Hall', 'Address', 'Walking Time']
    for i in range(len(header_list)):
        header.append((header_list[i], False))
    
    #creates return values
    tuple_list = []
    menu_list = []

    #finds info for dining halls
    b_list, b_menu = get_dining_hall("Bartlett", address)
    s_list, s_menu = get_dining_hall("South", address)

    #adds dining hall info to return values
    tuple_list.append(b_list)
    tuple_list.append(s_list)
    menu_list.append(b_menu)
    menu_list.append(s_menu)

    return (header, tuple_list, menu_list)


def drop():
    '''
    This code was only used for testing, drops the table yelp_results. 
    '''
    yelpapi.drop_yelp_table("yelp_results")

