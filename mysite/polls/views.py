from django.shortcuts import render

from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

from .models import Food_search

import sys
sys.path.insert(0, '/home/student/cs122project')


def search_form(request):
   
  return render(request, 'polls/search_form.html')

def search(request):
  error = []
  request_dict = {}
  if not request.GET['Cuisine'] == '':
    c = request.GET['Cuisine']
    request_dict['Cuisine'] = c
  else:
    request_dict['Cusine'] = None
  
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
  if request_dict['Types'] == []:
    error.append("Please Choose at least one of Restaurants, Food Trucks or Dinings Halls")
  
  if 'inspection' in request.GET:
    request_dict['inspection'] = True
  else:
    request_dict['inspection'] = False
  
  if not request.GET['walk_time'] == '':
    wt = request.GET['walk_time']
    request_dict['walk_time'] = wt
  else:
    request_dict['walk_time'] = False


  if error == []:
    food = Food_search(request_dict)
    return render(request, 'polls/search_results.html', {'food':food, 'query':m, 'location':a})
  return render(request, 'polls/search_form.html', {'errors':error})

def search_result(request):
  return render(request, 'polls/search_form.html')



#class SearchForm(forms.Form):

#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})

#def results(request, question_id):
 #   response = "You're looking at the results of question %s."
  #  return HttpResponse(response % question_id)

#def vote(request, question_id):
 #   return HttpResponse("You're voting on question %s." % question_id)

#def index(request):
 #   latest_question_list = Question.objects.order_by('-pub_date')[:5]
  #  template = loader.get_template('polls/index.html')
   # context = {
    #    'latest_question_list': latest_question_list,
    #}
    #return HttpResponse(template.render(context, request))