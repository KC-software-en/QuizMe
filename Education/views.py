# import render to render an HTML template with a given context and return an HttpResponse object
from multiprocessing import context
from unittest import result

# use get_object_or_404 in views.py to render a HTTP 404 error if a question with the requested ID doesn’t exist
from django.shortcuts import get_object_or_404, render

# import html to handle potential HTML entities and aid rendering
import html

# Import the login required decorator to prevent unaouthorised access to cetrain views.
from django.contrib.auth.decorators import login_required

# imported HttpResponseRedirect 
from django.http import HttpResponseRedirect

# imported reverse
from django.urls import reverse

# import get_json_categories for the index_edu view
from .utils import get_json_categories, get_specific_json_category, get_next_question_id

# import models
from .models import *

# import apps to dynamically fetch a model in detail() view
from django.apps import apps

# import Http404 to raise an error message if a model is not located in detail view
from django.http import Http404

# import random to shuffle questions in detail view, rendered in the form
import random

# import logging for debugging
import logging

#######################################################################################
#######################################################################################

# Create your views here.

'''
Create a view for the home page of QuizMe project.
'''
# define index view for home page of QuizMe project referenced in Education/urls.py
def index(request):     
    # Render your template and map a URL to it
    return render(request, "index.html")

'''
Create a view for the home page of education quizzes.
'''
# display the category of the education quiz
# https://www.youtube.com/watch?v=sgEhb50YSTE
# make the category_id a parameter set to None
# get json reponse for trivia categories from open trivia db
# index category from the dictionary id
def index_edu(request):
    # call the categories function & save its response in an assigned variable - NameError if you don't assign it
    response = get_json_categories()
    
    # get the trivia categories values from dictionary provided in json response
    # place an empty list as the default argument if the key is not found - should avoid errors in subsequent code
    trivia_categories = response.get("trivia_categories", [])

    # specify the id of the categories to include in the Education app's quizzes
    selected_category_id = [20]

    # collect the categories based on selected_category_id
    selected_categories = [category for category in trivia_categories if category.get("id") in selected_category_id]    

    # initialise a variable for the chosen category from the json response
    selected_category = None
    category_name = None

    # iterate over trivia categories to find the category id specified 
    for category in selected_categories:
        # check if the id in selected_category_id is in the trivia_categories
        if category.get("id") in selected_category_id:
            # assign the current category to the selected_category variable
            selected_category = category            
            
            # get the name of the category if the id exists for the selected category
            if selected_category:
                category_name = selected_category.get("name")
            
            # exit the loop when the desired category is found            
            break

    # the response is the dictionary for trivia categories
    # pass all the context variables into a single dictionary to render in the template correctly
    context = {'selected_category':selected_category, 'category_name': category_name}    
    return render(request, 'edu_quiz/edu_quiz.html', context) 

# write a view for the quiz question, incl the argument question_id
# question_id is the specific identifier passed in the URL when accessing this view
# it uniquely identifies and retrieves the specific question to display
# Django automatically adds an id field as the primary key for each model (i.e. question.id)
# display the question text 
# render an HTTP 404 error if a question with the requested ID doesn’t exist
def detail(request, category_name, question_id):    
    # use the category_name selected on edu_quiz.html to determine the model to get questions from
    # replace spaces in the event category names have spaces to create a valid model name
    model_name = category_name.replace(" ", "_")

    # use a try-except block to find a model that matches the category name
    # use apps module to dynamically retrieve a model
    # - dynamically:instead of explicitly specifying a fixed model in the code, generate or determine the model to use at runtime based on certain conditions/data
    try:
        model = apps.get_model('Education', model_name)
    except LookupError:
        raise Http404("Cannot locate the model for the selected category.")

    # get the 50 questions for the specific category
    # ##question_id is the specific identifier passed in the URL when accessing this view
    # ##it uniquely identifies and retrieves the specific question to display
    all_questions = model.objects.all()
    
    # create a list containing the pk for each obj
    category_question_ids = [question.id for question in all_questions]

    # get the ids for the selection of 10 questions
    # use random to select 10 questions
    # https://docs.python.org/3.7/library/random.html?highlight=random#random.sample
    # note: random.sample requires a list as its first argument
    question_selection_ids = random.sample(category_question_ids, 10)
    
    # filter the objects based on question_selection_ids
    question_selection = model.objects.filter(id__in=question_selection_ids)

    # use shuffle to mix questions each time
    random.shuffle(question_selection)    
    
    # render the edu_detail template & pass the 10 questions, their ids & category as context 
    context = {'question': question_selection, 
               'category_name': category_name, 
               'question_id':question_selection_ids}
    return render(request, 'edu_quiz/edu_detail.html', context)

'''
Create a view that displays the quiz result.
'''
# create a view that displays the quiz result 
def results(request, category_name): 
    # get the quiz result for the session
    result = request.session.get('quiz_result')
           
    # render the result template  
    # pass the quiz result for the session as a context variable
    context = {'result':result}   
    return render(request, 'edu_quiz/edu_result.html', context)

# write a view to answer a question, incl the argument question_id
# it handles the submitted data
def selection(request, category_name, question_id):    
    # pk refers to the primary key field of a database table
    # django automatically creates a primary key for each model
    model_name = category_name.replace(" ", "_")
    model = apps.get_model('Education', model_name)
    question = get_object_or_404(model, pk=question_id)

    # access submitted data by key name with a dictionary-like object- request.POST
    # use the key name choice which returns the ID of the selected choice
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice']
            )
    # raise a KeyError if the ID of the choice isn’t found
    # an error occurs if the mapping (dictionary) key was not located in the set of existing keys
    except (KeyError, model.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'edu_quiz/edu_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
            })
    else:
        # else add the point for a correct choice & save the choice
        # (in utils.py the id for the correct answer is 1)
        result = 0
        if selected_choice.id == question.correct_answer['id']:
            result += 1
            selected_choice.save()

        # get the next question
        next_question = get_next_question_id(category_name, question_id)

        # if there is another question available from the question_selection redirect to the detail view again
        # - to display that question 
        if next_question is not None:
            return HttpResponseRedirect(
                reverse('Education:edu_detail', category_name=category_name, question_id=next_question)
                )

        else:
            # store the calculated result in the session
            request.session['quiz_result'] = result

            # use HttpResponseRedirect instead of HttpResponse;
            # HttpResponseRedirect takes the URL to which the user will be redirected as an argument
            # Always return an HttpResponseRedirect after successfully
            # dealing with POST data. This prevents data from being
            # posted twice if a user hits the Back button.
            # use reverse function to take the name of the view and return the str value that represents the actual url                        
            return HttpResponseRedirect(
                reverse('Education:results', args=(category_name))
                )

# start new quiz function
def try_new_quiz(request):
    # delete the result & session data of the current quiz before starting a new quiz
    if 'quiz_result' in request.session:
        del request.session['quiz_result']

    # render the template for the home page of education      
    return HttpResponseRedirect(
                reverse('Education:index_edu')
                )  
        

