from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import sqlite3

auth = Oauth1Authenticator(
    consumer_key="yTQDnQbRRDkaCZigWaqv3A",
    consumer_secret="k91DCoNjymxAdAwC6tMhkPMHi6s",
    token="s4NScurjZlRzljVvRO-oy5xwdg-OBEgk",
    token_secret="uaLK5sh4mcilscg6q4Hm5DDUNfE"
)

client = Client(auth)

renoldslat, renoldslon = 41.7913324,-87.6001977

def yelp_by_coordinates(lat, lon, params):
    '''
    takes a latitude, longitude and a dictionary of paramiters and does a yelp 
    search and puts that search into a yelp_database
    the dictionary of parameters can have keys "term" and the 
    value will be a string with keywords for the search (eg sushi, burgers)
    '''
    results = client.search_by_coordinates(lat, lon, **params)
    
    
    table_string = "CREATE TABLE yelp_results (name varchar(50), latitude int, longitude REAL, rating real, address varchar(50), city varchar(25), state varchar(3), zip_code integer, phone_number integer);"

    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    db.execute(table_string)


    for i in range(len(results.businesses)):
        one_line = [results.businesses[i].name, str(results.businesses[i].location.coordinate.latitude), str(results.businesses[i].location.coordinate.longitude), str(results.businesses[i].rating), results.businesses[i].location.address[0], results.businesses[i].location.city, results.businesses[i].location.state_code, results.businesses[i].location.postal_code,results.businesses[i].phone]
        
      
        db.execute("Insert into yelp_results Values (?,?,?,?,?,?,?,?,?);", one_line)

    connection_yelp.commit()
    r = db.execute("Select * From yelp_results")
    
    return(r.fetchall())

def drop_yelp_table():
    '''
    deletes the yelp_results table in the yelp_database so there is no error
    the next time the create table statement is executed
    in yelp_by_coordinates
    '''

    connection_yelp = sqlite3.connect("yelp_database")
    db = connection_yelp.cursor()
    db.execute("drop table yelp_results")
    connection_yelp.close()
