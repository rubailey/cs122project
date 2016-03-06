from django import forms


def Food_search(search_params):
    '''
    takes a dictionary of search parameters and returns a list of food_option objects
    '''
    return[food_option(search_params).result]

class food_option(object):
    def __init__(self, line):
        '''
        takes in a result from a sqlite3 search and gives a class object where self.result
        is in the form which we want to return
        '''
        self.result = line

class SearchForm(forms.Form):
    Cuisine = forms.CharField()
    Menu_item = forms.CharField()
    Address = forms.CharField()
