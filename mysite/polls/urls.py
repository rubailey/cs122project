#this file is from django tutorial, code for urlpatterns is adapted from djangobook.com
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^search_form/$', views.search_form),
    # ...
]


