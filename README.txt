# cs122project
git repository for CS 122 winter 2016 Final Project
Hyde Park Lunchtime
Created by Russell Bailey and William Misener

This project will find a place to eat in Hyde Park. It includes capabilities for searching for restaurants, food trucks, and the UChicago Dining Halls. The user may (but does not have to) specify cuisine type, menu item search term, current address, whether to check for health inspection failures, maximum walking time from current location, and minimum yelp rating.

To run this code:
-You may need to install the Yelp API: run "sudo pip3 install yelp" to do so
-Starting from the cs122project directory, move into the mysite directory
-From the command line in ~/cs122project/mysite, enter "python3 manage.py runserver"
-Open a web browser and enter "http://127.0.0.1:8000/search_form/" as the url
-The results of the search are displayed as tables (the search may take some time)
-To make another search, click the "Search Again" button; this will return you to the original page
-occasionally there is a list index out of range error, this error will go away if you refresh the page, we are not sure of the cause of this error as it is from the google maps api

The search will run with no parameters, but is limited to max. 20 results per section. However, if none of Restaurants, Food Trucks, or Dining Hall is selected, the search will return you to the search page with a warning to select at least one.

We created the django code using tutorials from https://docs.djangoproject.com/en/1.9/intro/tutorial01/ and http://www.djangobook.com/en/2.0/chapter07.html most of the code from these two tutorials was adapted to fit our project, but some of it was kept. The djangoproject.com tutorial had us download the entire mysite file (which we then added our own files into) but some of the files we downloaded are never called by our code but we were not sure if deleting them would cause django to break. Manage.py was taken entirely from djangoproject.com and was not modified. We also used http://www.w3schools.com for help with HTML but no code was taken directly from it. 
 
General overview of code structure:
When a search is entered, search(request) in polls/views.py is called with the request.
This creates a dictionary with the search params, which is passed into models.py.
Food_search(search_params) calls various other helper functions separately based on which search parameters are specified by the user; these functions are explained in more detail in their respective doc strings.
Food_search outputs a list of search results, which are output onto the screen by ~/cs122project/mysite/polls/templates/polls/search_results.html.



