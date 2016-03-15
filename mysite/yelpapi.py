'''
The first part of this code is from github.com/yelp/yelp-python, gives
information on how to get the client using the identifiers. 
The line client.search(location, **params), abd the equlivelent for search by 
coordinates were also taken from this page, information on how the paramerters 
works is from www.yelp.com/developers/documentation

found out about SequenceMatcher from http://stackoverflow.com/questions/4802137/how-to-use-sequencematcher-to-find-similarity-between-two-strings
takes code given as answer and manipulates it in reasonable_permutation
'''
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from google_dist import get_distance
from food_truck import scrap_food_trucks
from difflib import SequenceMatcher
import sqlite3


auth = Oauth1Authenticator(
    consumer_key="yTQDnQbRRDkaCZigWaqv3A",
    consumer_secret="k91DCoNjymxAdAwC6tMhkPMHi6s",
    token="FdD-kVCiIo1c7SVOWkS2zgyp3D-JNuqA",
    token_secret="b8IjKRe8Yqj4HPIKLE3_kts7-Jw"
)

client = Client(auth)

renoldslat, renoldslon = 41.7913324,-87.6001977

def yelp_search(location, term=None, coordinates=False):
    '''
    takes a location, optional term and whether the location is coordinates
    and does a yelp search and puts that search into a yelp_database
    term should be a string, location will most likely be a string
    Food_search only deals with location as a string, but coordinates are 
    helpful for testing. 
    '''
    #params dictionary for yelp search
    params = {"category_filter":"restaurants"}
    if not term == None:
        params["term"] = term
    
    #handles if searching with coordinates or not
    if coordinates:
        lat, lon = location
        location = str(lat) + " " + str(lon)
        results = client.search_by_coordinates(lat, lon, **params)
    else:
        results = client.search(location, **params)
    
    #string to create table
    table_string = "CREATE TABLE yelp_results (name varchar(50), latitude real, longitude real, rating real, address varchar(50), city varchar(25), state varchar(3), zip_code integer, phone_number integer, distance varchar(10), walking_time int) ;"

    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    
    #if the code fails unexpectedly or is quitted out an error will be thrown because
    #the table never gets deleted, this solves that issue
    try:
        db.execute(table_string)
    except:
        db.execute("drop table yelp_results")
        db.execute(table_string)

    #results.businesses is a list of the buisinesses, this loops over it
    for i in range(len(results.businesses)):
        if not(results.businesses[i].location.coordinate == None or results.businesses[i].location.address == []):
            #calls get_distance to get distance and walking time
            distance, walking_time = get_distance(location, results.businesses[i].location.address[0] +", "+ results.businesses[i].location.city)
            
            #turns walking time into minutes, gets rid of "mins" at end so it is an integer
            if not 'hour' in walking_time:
                walking_time = int(walking_time.split()[0])
            else:
                walking_time = 60*int(walking_time.split()[0]) + int(walking_time.split()[2])
            
            #creates line and executes it to make a row in the yelp_results table
            one_line = [results.businesses[i].name, str(results.businesses[i].location.coordinate.latitude), str(results.businesses[i].location.coordinate.longitude), str(results.businesses[i].rating), results.businesses[i].location.address[0], results.businesses[i].location.city, results.businesses[i].location.state_code, results.businesses[i].location.postal_code,results.businesses[i].phone, distance, walking_time]
            db.execute("Insert into yelp_results Values (?,?,?,?,?,?,?,?,?,?,?);", one_line)
            
    connection_yelp.commit()
    db.close()
    #this function returns nothing, only creates a table


def yelp_search_food_trucks(location, term=None):
    '''
    takes a location and a search term (string) and does a yelp 
    search and puts that search into a yelp_database
    returns nothing, only creates the yelp table
    '''

    #params dictionary for yelp search (only searches foodtrucks)
    params = {"category_filter":"foodtrucks"}
    if not term == None:
        params["term"] = term

    results_list = []

    #searches yelp always with location chicago, food trucks have no location in hyde park
    results_list.append(client.search("Chicago", **params))

    #seees how many searches of 20 will get full list
    iterations = round(results_list[0].total/20 +.4999999)
   
    #since foodtrucks have no locations, yelps first 20 results are
    #not always what we want, so we do multiple searches 
    for num in range(1,iterations):
        params['offset'] = 20*num
        results_list.append(client.search("Chicago", **params))


    table_string = "CREATE TABLE yelp_food_trucks (name varchar(50), rating real, phone_number integer, distance varchar(10), walking_time int, arrive_time varchar(5), leave_time varchar(5));"

    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()

    #accounds for occasional error in same mannar as with restaurants
    try:
        db.execute(table_string)
    except:
        db.execute("drop table yelp_food_trucks")
        db.execute(table_string)

    #all food trucks are on near 58th and University according to food truck finder, uses this address for walking time
    distance, walking_time = get_distance(location, "5800 University, Chicago, IL")
    
    #makes walking time a integer of minutes
    if not 'hour' in walking_time:
        walking_time = int(walking_time.split()[0])
    else:
        walking_time = 60*int(walking_time.split()[0]) + int(walking_time.split()[2])
    
    #scrapes website for which foodtrucks are available today
    trucks_today, truck_dict = scrap_food_trucks()
    
    #needs the extra loop because occasionally more than one results to loop over (4 in the case of no search term)
    for results in results_list:
        for i in range(len(results.businesses)):
            
            #Occasionally names from yelp and foodtruck finders are slightly different
            key = reasonable_permutation(results.businesses[i].name, trucks_today)
            
            #if foodtruck is present, will be true, creates line it table for the truck
            if not key == None:
                arrive, leave = truck_dict[key]
                one_line = [results.businesses[i].name, str(results.businesses[i].rating),results.businesses[i].phone, distance, walking_time, arrive, leave]
                db.execute("Insert into yelp_food_trucks Values (?,?,?,?,?,?,?);", one_line)
            
    connection_yelp.commit()
    db.close()
    #this function does nothing, only creates a table

def drop_yelp_table(table):
    '''
    deletes the yelp_results table in the yelp_database so there is no error
    the next time the create table statement is executed
    in yelp_by_coordinates
    '''

    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    db.execute("drop table "+ table)
    connection_yelp.close()

def reasonable_permutation(truck_name, name_list):
    '''
    takes the name from yelp and the list of truck names from foodtruck finders
    returns either the name on foodtruck finders or None if not present
    '''
    #makes strings lower
    name = truck_name.lower()
    for one in name_list:
        #uses .85 as minimum similarness threshold
        if SequenceMatcher(None, name, one.lower()).ratio()>.85:
            return one
    return None
    




