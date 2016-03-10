from django import forms
import sqlite3
import yelpapi
import menu_scraper
import dining_scraper
import google_dist

DEFAULT_WALK_TIME = 25
DEFAULT_ADDRESS = '1100 E 57th St, Chicago, IL'
def Food_search(search_params):
    '''
    takes a dictionary of search parameters and returns a list of lists of lists
    '''
    rv = []

    #drop()
    if search_params['Address'] == None:
        address = DEFAULT_ADDRESS
    else:
        if not 'Chicago' in search_params['Address']:
            address = search_params['Address'] + ', Chicago, IL'

    cuisine = search_params['Cuisine']

    menu_item = search_params['Menu_item']

    walk_time = search_params['walk_time']

    inspection = search_params['inspection']
    if walk_time == False:
        walk_time = DEFAULT_WALK_TIME

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
                    truck_dict[name] = (url)
        
    if 'Restaurants' in search_params['Types']:
        header, options = find_restaurants(address, cuisine, walk_time, inspection)
        options_r = [(header, True)]
        appended_list = []
        for op in options:
            if not op[0] in appended_list:
                mini_list = []
                for i in range(len(op)):
                    mini_list.append((op[i], False))
                if not menu_item == None:
                    menu = menu_scraper.scrape_rest(rest_dict, op[1])
                    if type(menu) == str:
                        mini_list.append(([menu], True))
                    else:
                        items = dining_scraper.search_menu(menu, menu_item)
                        if items == []:
                            items = "No Menu Items Matched"
                            mini_list.append(([items], True))
                        elif len(items) > 5:
                            items = items[:5]
                            mini_list.append((items, True))
                        else:
                            mini_list.append((items, True))
                options_r.append((mini_list, False))
                appended_list.append(op[0])
        if not menu_item == None:
            options_r[0][0].append(('Menu Items', False))


        rv.append(options_r)

    if 'Food_trucks' in search_params['Types']:
        header, options = find_food_trucks(address, cuisine, walk_time)
        options_ft = [(header, True)]
        appended_list = []
        for op in options:
            if not op[0] in appended_list:
                mini_list = []
                for i in range(len(op)):
                    mini_list.append((op[i], False))
                if not menu_item == None:
                    menu = menu_scraper.scrape_rest(truck_dict, op[0])
                    if type(menu) == str:
                        mini_list.append(([menu], True))
                    else:
                        items = dining_scraper.search_menu(menu, menu_item)
                        if items == []:
                            items = ["No Menu Items Matched"]
                        elif len(items) > 5:
                            items = items[:5]
                        mini_list.append((items, True))
                options_ft.append((mini_list, False))
                appended_list.append(op[0])
        if not menu_item == None:
            options_ft[0][0].append(('Menu Items', False))
        print (options_ft)
        rv.append(options_ft)

        

    if 'Dining_hall' in search_params['Types']:
        header, options, menus = find_dining_halls(address)
        
        options_dh = [(header, True)]
        if not menu_item == None:
            header.append(("Menu Items", False))
            for i in range(len(options)):
                mini_list = []
                for x in range(len(options[i])):
                    mini_list.append((options[i][x], False))

                if not menu_item == None:
                    items = dining_scraper.search_menu(menus[i], menu_item)
                    if items == []:
                        items = ["No Menu Items Matched"]
                    elif len(items) > 5:
                        items = items[:5]
                    mini_list.append((items, True))
                options_dh.append((mini_list, False))
        print (options_dh)
        rv.append(options_dh)

    return rv



def find_restaurants(address, cuisine, walk_time, inspection, rating=None):
    '''
    Takes parameters and searches for restaurants matching the search criteria.
    Returns a list of food_option objects.
    '''

    yelpapi.yelp_search(address, cuisine)
    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    header = []
    selectline = 'SELECT yelp_results.name, yelp_results.address, yelp_results.rating, yelp_results.phone_number, yelp_results.walking_time'
    header_list = ['Restaurants', 'Address', 'Rating', 'Phone', 'Walking Time']
    for i in range(len(header_list)):
        header.append((header_list[i], False))

    fromline = ' FROM yelp_results'
    whereline = ' WHERE yelp_results.walking_time < ?'
    if inspection:
        selectline += ', healthfails.Risk'
        header.append('Risk')
        fromline += ' LEFT OUTER JOIN healthfails ON yelp_results.address=healthfails.Address COLLATE NOCASE'

    end_list = [walk_time]
    if not rating == None:
        whereline += ' and yelp_results.rating >= ?'
        end_list.append(rating)
    print(selectline + fromline + whereline, [walk_time])
    r = db.execute(selectline + fromline + whereline + ';', end_list)
    tuple_list = r.fetchall()
    yelpapi.drop_yelp_table("yelp_results")
    db.close()
    return (header,tuple_list)

def find_food_trucks(address, cuisine, walking_time, rating = None):
    yelpapi.yelp_search_food_trucks(address, cuisine)
    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()

    selectline = 'SELECT yelp_food_trucks.name, yelp_food_trucks.rating, yelp_food_trucks.phone_number, yelp_food_trucks.arrive_time, yelp_food_trucks.leave_time'
    header = []
    header_list = ['Food Trucks', 'Rating', 'Phone', 'Arrive Time', 'Depart Time']
    for i in range(len(header_list)):
        header.append((header_list[i], False))
    fromline = ' FROM yelp_food_trucks'
    whereline = ' WHERE yelp_food_trucks.walking_time < ?'
    end_list = [walking_time]
    if not rating == None:
        whereline += ' and yelp_food_trucks.rating >= ?'
        end_list.append(rating)
    print(selectline + fromline + whereline + ';', end_list)
    r=db.execute(selectline + fromline + whereline + ';', end_list)
    tuple_list = r.fetchall()
    db.close()
    yelpapi.drop_yelp_table("yelp_food_trucks")
    return (header, tuple_list)

def get_dining_hall(hall, address):
    addresses = {"Bartlett": "5640 S University Ave", "South": "6025 S Ellis Ave"}
    menu = dining_scraper.find_dining_menu_items(hall, "Lunch")
    if menu == []:
        menu = dining_scraper.find_dining_menu_items(hall, "Brunch")
    dh_addr = addresses[hall] + ", Chicago"
    dist, time = google_dist.get_distance(address, dh_addr)
    if not 'hour' in time:
        time = int(time.split()[0])
    else:
        time = 60*int(time.split()[0]) + int(time.split()[2])
           
    return [hall + " Dining Hall", addresses[hall], time], menu

def find_dining_halls(address):
    header = []
    header_list = ['Dining Hall', 'Address', 'Walking Time']
    for i in range(len(header_list)):
        header.append((header_list[i], False))
    tuple_list = []
    menu_list = []
    b_list, b_menu = get_dining_hall("Bartlett", address)
    s_list, s_menu = get_dining_hall("South", address)
    tuple_list.append(b_list)
    tuple_list.append(s_list)
    menu_list.append(b_menu)
    menu_list.append(s_menu)

    return (header, tuple_list, menu_list)


def drop():
    yelpapi.drop_yelp_table("yelp_results")

