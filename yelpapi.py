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
    takes a latitude, longitude and a dictionary of paramiters and does a yelp 
    search and puts that search into a yelp_database
    the dictionary of parameters can have keys "term" and the 
    value will be a string with keywords for the search (eg sushi, burgers)
    '''
    params = {"category_filter":"restaurants"}
    if not term == None:
        params["term"] = term
    print (params)

    if coordinates:
        lat, lon = location
        location = str(lat) + " " + str(lon)
        results = client.search_by_coordinates(lat, lon, **params)
    else:
        results = client.search(location, **params)

    drop_yelp_table("yelp_results")
    table_string = "CREATE TABLE yelp_results (name varchar(50), latitude int, longitude REAL, rating real, address varchar(50), city varchar(25), state varchar(3), zip_code integer, phone_number integer, distance varchar(10), walking_time varchar(10));"

    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    db.execute(table_string)

    for i in range(len(results.businesses)):
        
        if not(results.businesses[i].location.coordinate == None or results.businesses[i].location.address == []):
            distance, walking_time = get_distance(location, results.businesses[i].location.address[0] +", "+ results.businesses[i].location.city)
            one_line = [results.businesses[i].name, str(results.businesses[i].location.coordinate.latitude), str(results.businesses[i].location.coordinate.longitude), str(results.businesses[i].rating), results.businesses[i].location.address[0], results.businesses[i].location.city, results.businesses[i].location.state_code, results.businesses[i].location.postal_code,results.businesses[i].phone, distance, walking_time]
            db.execute("Insert into yelp_results Values (?,?,?,?,?,?,?,?,?,?,?);", one_line)
            
    connection_yelp.commit()
    r = db.execute("Select * From yelp_results")
    
    return(r.fetchall())

def yelp_search_food_trucks(location, term=None):
    '''
    takes a latitude, longitude and a dictionary of paramiters and does a yelp 
    search and puts that search into a yelp_database
    the dictionary of parameters can have keys "term" and the 
    value will be a string with keywords for the search (eg sushi, burgers)
    '''
    params = {"category_filter":"foodtrucks"}
    if not term == None:
        params["term"] = term
    print (params)

    results = client.search("Chicago", **params)

    drop_yelp_table("yelp_food_trucks")
    table_string = "CREATE TABLE yelp_food_trucks (name varchar(50), rating real, phone_number integer, distance varchar(10), walking_time varchar(10), arrive_time varchar(5), leave_time varchar(5));"

    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    db.execute(table_string)

    #all food trucks are on near 58th and University
    distance, walking_time = get_distance(location, "5800 University, Chicago, IL")
    trucks_today, truck_dict = scrap_food_trucks()
    print(trucks_today)
    for i in range(len(results.businesses)):
        print (results.businesses[i].name)
        key = reasonable_permutation(results.businesses[i].name, trucks_today)
        if not key == None:
            arrive, leave = truck_dict[key]
            one_line = [results.businesses[i].name, str(results.businesses[i].rating),results.businesses[i].phone, distance, walking_time, arrive, leave]
            db.execute("Insert into yelp_food_trucks Values (?,?,?,?,?,?,?);", one_line)
            
    connection_yelp.commit()
    r = db.execute("Select * From yelp_food_trucks")
    
    return(r.fetchall())

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
    name = truck_name.lower()
    for one in name_list:
        if SequenceMatcher(None, name, one.lower()).ratio()>.85:
            return one
    return None
    




