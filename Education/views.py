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
Create a view for the home page of QuizMe project.
'''
# define index view for home page of QuizMe project referenced in Education/urls.py
def index(request): 
    # comment out HttpResponse once confirmed the page shows        
    # Render your template and map a URL to it
    return render(request, "index.html")

'''
Create a function that returns the json response for the available categories on Open Trivia DB.
'''
# define a function that returns the json response for Open Trivia DB
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

'''
Create a view for the home page of education quizzes.
'''
# display the category of the education quiz
# https://www.youtube.com/watch?v=sgEhb50YSTE
# get json reponse for trivia categories from open trivia db
# index category from the dictionary id
def index_edu(request, category_id=20):
    # call the categories function & save its response in an assigned variable - NameError if you don't assign it
    response = get_json_categories()
    
    # get the trivia categories values from dictionary provided in json response
    # place an empty list as the default argument if the key is not found - should avoid errors in subsequent code
    trivia_categories = response.get("trivia_categories", [])

    # initialise a variable for the chosen category from the json response
    selected_category = None
    category_name = None

    # iterate over trivia categories to find the category id specified in the function as a parameter
    for category in trivia_categories:
        # cast category_id to int for error handling
        if category.get("id") == int(category_id):
            # assign the current category to the selected_category variable
            selected_category = category            
            
            # get the name of the category if the id exists for the selected category
            if selected_category:
                category_name = selected_category.get("name")
            
            # exit the loop when the desired category is found            
            break

    # the response is the dictionary for trivia categories
    # pass all the context variables into a single dictionary to render in the template correctly
    return render(request, 'edu_quiz/edu_quiz.html', {'selected_category':selected_category, 'category_name': category_name}) 

'''
Create a function that returns the json response for a specific category on Open Trivia DB.
'''
# define a function that returns the json response for Open Trivia DB when requesting a specific category
# create a varible to store the API url for the myth quizzes
# use an f-str to pass in the parameter for quantity
# -> place {} around 50 in the url then replace '50' with 'quantity'
# then place {} around the category id (from quiz_cat.json)for myth & replace '20' with 'category'
# return a list
def get_specific_json_category(quantity: int, category: int):
    mythology_url = f"https://opentdb.com/api.php?amount={quantity}&category={category}"
    response = requests.get(mythology_url)

    return response