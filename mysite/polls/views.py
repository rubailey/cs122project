from django.shortcuts import render

from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

from .models import Food_search, SearchForm


def search_form(request):
   
  return render(request, 'polls/search_form.html')

def search(request):
  error = False
  request_dict = {}
  if 'Cusine' in request.GET:
      c = request.GET["Cusine"]
      request_dict["Cusine"] = c
      if not c:
        error = True
  if 'Menu_item' in request.GET:
      m = request.GET["Menu_item"]
      request_dict["Menu_item"] = m
      if not m:
        error = True
  if 'Address' in request.GET:
      a = request.GET["Address"]
      request_dict["Address"] = a
      if not a:
        error = True
  if 'Food_trucks' in request.GET:
      ft = request.GET['Food_trucks']
      request_dict['Food_trucks'] = ft
  if 'Dining_hall' in request.GET:
      dh = request.GET['Dining_hall']
      request_dict['Dining_hall'] = dh
  if 'Restaurants' in request.GET:
      r = request.GET['Restaurants']
      request_dict['Restaurants'] = r
  if 'inspection' in request.GET:
      p = request.GET['inspection']
      request_dict['inspection'] = p
  if not error:
    food = Food_search(request_dict)
    return render(request, 'polls/search_results.html', {'food':food, 'query':m, 'location':a })
  return render(request, 'polls/search_form.html', {'error':error})



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