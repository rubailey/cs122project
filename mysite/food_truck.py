'''
All code here is original
'''

import requests
import bs4
import re
import datetime

def scrap_food_trucks():
    '''
    scrapes the url for food truck finders weekly scedule
    retuns tuple with a list of trucks and a dictionary that maps those trucks to 
    their arrive and leave times
    '''
    #Weekly scedule has info for whole week (usually not accurate up to the day)
    #these are keys to turn number into week days
    Days_of_Week = ["Sunday", "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday", "Sunday"]
    truck_dict = {}
    
    #always the url on the week day, requests and beautiful soups it
    url = "http://www.chicagofoodtruckfinder.com/weekly-schedule"
    r = requests.get(url)
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    rows = soup.find_all("tr")
    header = rows[0]
    
    #looks through rows in table to find one with name "University of Chicago"
    for i in range(1,len(rows)):
        colls = rows[i].find_all("td")
        if colls[0].text.strip() == "University of Chicago":

            #creates a dictionary mapping day of week to trucks there on that day
            for j in range(1, len(colls)):
                truck_dict[Days_of_Week[j-1]] = colls[j]
    
    #uses datetime to find what day it is today, thus find which trucks are available on that day
    current_dow = Days_of_Week[datetime.date.isoweekday(datetime.date.today())]
    truck_list = truck_dict[current_dow].find_all("a")
    
    #re search patterns 
    search_pat = "title.*/>"
    search_time = "[0-9][0-9]:[0-9][0-9] [A-Z]M"
    rv = ([],{})
    
    #loops through trucks and appends each one to the return list and dicitonary
    for truck in truck_list:
        string = re.search(search_pat, str(truck)).group()
        start, end = re.findall(search_time, string)

        #this is the name of truck, scrapes away other part of text line
        #27,-3 come from the line begining with title='10:30 AM - 02:00 PM (same number of characters for any time) and ending with '>/ (always the same)
        name = string[27:-3]
        rv[0].append(name)
        rv[1][name] = (start, end)

    return rv

