from django.shortcuts import render

# import HttpResponse then comment out after confirming the views rendered
# import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect

# import the Question model
from .models import Question, Choice

# the view renders an HTTP 404 error if a question with the requested ID doesn’t exist.
# import render
from django.shortcuts import get_object_or_404, render

# import reverse to generate a URL for a given view function 
# to avoid hardcoding URLs in the code, making the app more maintainable and flexible
from django.urls import reverse

# import requests to use the API for edu quiz
import requests

# import html to handle potential HTML entities and aid rendering
import html

# import random to shuffle choices rendered in the form
import random

# import json to work with the data retrieved from the open trivia db API
import json

#######################################################################################
#######################################################################################

# Create your views here.

'''
'''
# define index view for home page of QuizMe project referenced in Education/urls.py
def index(request): ############################################################add here
    # comment out HttpResponse once confirmed the page shows        
    # Render your template and map a URL to it
    return render(request, "index.html")

'''
'''
#
def get_json_categories():
    # get Category Lookup url
    category_lookup = 'https://opentdb.com/api_category.php'
    # store url in a variable as a json response
    response = requests.get(category_lookup).json()

    # write Categories to a json file
    # use an indent to ensure each category prints on separate lines
    with open("quiz_categories.json", "w") as f:
        json.dump(response, f, indent=4)

    return response
