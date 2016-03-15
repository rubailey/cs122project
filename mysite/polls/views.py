from django.shortcuts import render

from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

from .models import Food_search

import sys
sys.path.insert(0, '/home/student/cs122project')


def search_form(request):
  #calls html teplate for search_form
  return render(request, 'polls/search_form.html')

def search(request):
  '''
  goes through each possible imput, if in request.GET adds to dictionary with what the user inputed
  if not in request.GET adds to dicitonary with a null or default value
  '''
  error = None
  request_dict = {}
  

  if not request.GET['Cuisine'] == '':
    c = request.GET['Cuisine']
    request_dict['Cuisine'] = c
  else:
    request_dict['Cuisine'] = None
  
  if not request.GET['Menu_item'] == '':
    m = request.GET['Menu_item']
    request_dict['Menu_item'] = m
  else:
    request_dict['Menu_item'] = None
    m = 'Food'

  if not request.GET['Address'] == '':
    a = request.GET['Address']
    request_dict['Address'] = a
  else:
    request_dict['Address'] = None
    a = "UChicago"

  request_dict['Types'] = []
  if 'Food_trucks' in request.GET:
    ft = request.GET['Food_trucks']
    request_dict['Types'].append(ft)
  if 'Dining_hall' in request.GET:
    dh = request.GET['Dining_hall']
    request_dict['Types'].append(dh)
  if 'Restaurants' in request.GET:
    r = request.GET['Restaurants']
    request_dict['Types'].append(r)
  
  #creates error if none of trucks, dinnig halls or restaurants was chosen
  if request_dict['Types'] == []:
    error = "Please Choose at least one of Restaurants, Food Trucks or Dining Halls"
  
  if 'inspection' in request.GET:
    request_dict['inspection'] = True
  else:
    request_dict['inspection'] = False
  
  if not request.GET['walk_time'] == '':
    wt = request.GET['walk_time']
    request_dict['walk_time'] = wt
  else:
    request_dict['walk_time'] = False
  request_dict['Rating'] = request.GET['Rating']

  #if an error was not found
  if error == None:
    food = Food_search(request_dict)
    return render(request, 'polls/search_results.html', {'food':food, 'query':m, 'location':a})
  
  #returns to search form and shows the error
  return render(request, 'polls/search_form.html', {'errors':error})

def search_result(request):
  #search again button in search result goes back to empty search form
  return render(request, 'polls/search_form.html')


