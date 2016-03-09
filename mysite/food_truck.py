import requests
import bs4
import re
import datetime

def scrap_food_trucks():
    Days_of_Week = ["Sunday", "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday", "Sunday"]
    truck_dict = {}
    url = "http://www.chicagofoodtruckfinder.com/weekly-schedule"
    r = requests.get(url)
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    rows = soup.find_all("tr")
    header = rows[0]
    for i in range(1,len(rows)):
        colls = rows[i].find_all("td")
        if colls[0].text.strip() == "University of Chicago":
            for j in range(1, len(colls)):
                truck_dict[Days_of_Week[j-1]] = colls[j]
    
    current_dow = Days_of_Week[datetime.date.isoweekday(datetime.date.today())]
    truck_list = truck_dict[current_dow].find_all("a")
    search_pat = "title.*/>"
    search_time = "[0-9][0-9]:[0-9][0-9] [A-Z]M"
    rv = ([],{})
    for truck in truck_list:
        string = re.search(search_pat, str(truck)).group()
        start, end = re.findall(search_time, string)
        name = string[27:-3]
        rv[0].append(name)
        rv[1][name] = (start, end)

    return rv

#food_truck_MP{}