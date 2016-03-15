'''
All original code
Contains code to get the distance between two addresses
'''

import requests
import json

def get_distance(add1, add2):
    '''
    Takes two addresses and uses Google Maps Distance Matrix to find the 
    distance and walking time between two addresses
    Inputs:
        add1, add2: strings that contain addresses or locations (Google is flexible)
    Output:
        a tuple of the distance and walking time between the two points, as calculated by Google
    '''

    # maps key hardcoded in, as is walking mode and imperial units
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?mode=walking&units=imperial&origins=" + add1 + "&destinations=" + add2 + "&key=AIzaSyCd69fBTN9dJ0R37EEzzHxupQA98OZDWOg"
    r = requests.get(url)
    page = r.text
    
    # turns json returned by search into Python dictionary
    distdict = json.loads(page)
    dist = distdict['rows'][0]['elements'][0]['distance']['text']
    time = distdict['rows'][0]['elements'][0]['duration']['text']
    
    return (dist, time)