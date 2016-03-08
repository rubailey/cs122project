import requests
import json

def get_distance(add1, add2):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?mode=walking&units=imperial&origins=" + add1 + "&destinations=" + add2 + "&key=AIzaSyCd69fBTN9dJ0R37EEzzHxupQA98OZDWOg"
    r = requests.get(url)
    page = r.text
    distdict = json.loads(page)
    dist = distdict['rows'][0]['elements'][0]['distance']['text']
    time = distdict['rows'][0]['elements'][0]['duration']['text']
    return (dist, time)