# import render to render an HTML template with a given context and return an HttpResponse object
from multiprocessing import context
from unittest import result
from django.shortcuts import render

# import requests to use the API for edu quiz
import requests

# import html to handle potential HTML entities and aid rendering
import html

# import random to shuffle choices rendered in the form
import random

# import json to work with the data retrieved from the open trivia db API
import json

# Import the login required decorator to prevent unaouthorised access to cetrain views.
from django.contrib.auth.decorators import login_required

# import HttpResponseRedirect
from django.http import HttpResponseRedirect

# import reverse
from django.urls import reverse

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
Create a function that returns the json response for the available categories on Open Trivia DB.
'''
# define a function that returns the json response for Open Trivia DB
def get_json_categories():
    # get Category Lookup url
    category_lookup = 'https://opentdb.com/api_category.php'
    # store url in a variable as a json response
    response = requests.get(category_lookup)
    if response.status_code == 200:
        json_response = response.json()
    
        # write Categories to a json file
        # use an indent to ensure each category prints on separate lines
        with open("quiz_categories.json", "w") as f:
            json.dump(json_response, f, indent=4)

        return json_response
    
    else:
        # print error if unsuccessful request
        # return None to signal that there's no valid data to work with
        error_message = f"Unable to retrieve the specific category - Status code:{response.status_code}"
        print(error_message)
        return None

'''
Create a view for the home page of education quizzes.
'''
# display the category of the education quiz
# https://www.youtube.com/watch?v=sgEhb50YSTE
# get json reponse for trivia categories from open trivia db
# index category from the dictionary id
# Add tjhe login required decorator to prevent access to the index_edu view.
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
# -> place {} around 5 in the url then replace '5' with 'quantity'
# then place {} around the category id (from quiz_cat.json)for myth & replace '20' with 'category'
# return a list
def get_specific_json_category(quantity: int, category: int):
    mythology_url = f"https://opentdb.com/api.php?amount={quantity}&category={category}"
    response = requests.get(mythology_url)
    
    # a successful request will give a 200 status code
    # get a json response or else there will only be a status code        
    if response.status_code == 200:
        json_response = response.json()
    
        # write chosen category to a json file - has to be after getting a json response (converting to a dictionary) 
        # - because writing to a file needs to be done on a serialisable object
        # use an indent to ensure each category prints on separate lines
        with open("chosen_quiz_category.json", "w") as f:
            json.dump(json_response, f, indent=4)

        return json_response

    else:
        # print error if unsuccessful request
        # return None to signal that there's no valid data to work with
        error_message = f"Unable to retrieve the specific category - Status code:{response.status_code}"
        print(error_message)
        return None    

# rearrange the options of answers
# use the random module & its shuffle function to rearrange
# return a list of choices
def mix_choices(choices: list):
    random.shuffle(choices)
    return choices

'''
Create a function to generate a selection of questions & choices from the selected category.
'''
# create a function to generate a selection of questions
# include parameters (expected variables) for the number of questions you want & the category for them
def get_questions_and_choices(request, quantity:int, category:int):
    # call the specific category function & save its response in an assigned variable - NameError if you don't assign it
    json_response = get_specific_json_category(quantity=5, category=20)

    # check if there are questions
    if json_response:        
        # save json response as a variable to pass into template
        questions = json_response["results"]

        # check if question retrieval was successful
        if questions:
            # iterate over each question in the results dictionary 
            for question in questions:                        
                # add new question text key for each question in results dictionary(AKA questions) by indexing its key                
                # - index question text - access the value associated with the key "question" in each dictionary
                # - use html.unescape to handle potential HTML entities and ensure accurate rendering in templates
                question["question_text"] = html.unescape(question["question"]) 
            
                # iterate over the incorrect answers with html.unescape and place them into a list with list comprehension                
                # use html.unescape & handle potential HTML entities for accurate rendering of templates
                # place the answers from the response in a variable - index it from the list of key:value pairs available for each question(result)
                choice_texts = [html.unescape(answer) for answer in question["incorrect_answers"]] 
                # use html.unescape for the correct answer
                # add the correct answer to the list of incorrect answers
                choice_texts.append(html.unescape(question["correct_answer"]))

                # call the function to rearrange choices and make the extended choice list the argument
                mixed_choices = mix_choices(choice_texts)            

                # save the mixed choices to each question in the results dictionary        
                # add a key-value pair to the question dictionary (from the category json response)
                question['mixed_choices'] = mixed_choices

            # assign a context dictionary that will be passed as an argument in template
            # intended to be calculated in subsequent views (such as selection and results), include result & question_quantity in the context with default values of None
            context = {'questions': questions,                       
                       'mixed_choices': mixed_choices, 
                       'error_message': None,
                       'result': None,
                       'question_quantity': None
                       }
            
            # return the list of dictionaries in the json response which contains the questions/answers
            # note the json response is a dictionary where its :value ("results") contains a list of dictionaries            
            return render(request, 'edu_quiz/edu_detail.html', context)

        # render error message if no questions were found
        else:
            error_message = f"Unable to retrieve the questions from the json response" 
            context = {'questions': None,                       
                       'mixed_choices': None, 
                       'error_message': error_message,
                       'result': None,
                       'question_quantity': None}            
            return render(request, 'edu_quiz/edu_detail.html', context)                        

# create a function to calculate the quiz result
# pass request object as an argument to resolve NameError: name 'request' is not defined - pass explicitly        
# make the questions and the user's selection the arguments needed to calculate the score      
def calculate_result(request, questions, user_selections):
    # set the counter for the results
    result = 0   

    for question in questions:
        # assign an ID for each question in a form that has request.POST
        # where question_ is the string literal prefix of the key id & embed the index for 'question' from the results (AKA questions) dictionary
        question_id = f"question_{question['question']}"

        # use html.unescape & handle potential HTML entities for accurate rendering of templates
        # place the answers from the response in a variable - index it from the list of key:value pairs available for each question(result)
        correct_answer = html.unescape(question["correct_answer"])
        
        # try checking if the user's selected choice for a specific question, identified by the constructed q_id, matches the correct answer for that question in the questions dictionary
        # add a point to the score
        try:                
            if (question_id in user_selections) and (user_selections[question_id] == correct_answer):
                result += 1   
        
        # raise an error if the user has not selected a choice
        # redisplay the quiz form
        except(KeyError):
            return render(request, 'edu_quiz/edu_detail.html', 
                          {
                              'questions': questions,
                              'mixed_choices':None,
                              'error_message': "You didn't select a choice.",
                              'result': None,
                              'question_quantity': None
                              }
                              )
    
    # return result for the results view
    return result

# create a view that displays the quiz result 
def results(request, result, question_quantity):    
    # get the data for each question & its selected choice
    # pass the data as a context variable in the results template
    # render the result template 
    context = {'result': result,
                'question_quantity': question_quantity}
    return render(request, 'edu_quiz/edu_result.html', context)

# create a view that saves your selected choice
def selection(request):
    # initialise context with default values # to fix error but it didnt work
    context = {'error_message': None,
               'questions': None,
               'mixed_choices': None,
               'result': None,
               'question_quantity': None
               }
    
    if request.method == "POST":                
        json_response = get_specific_json_category(quantity=5, category=20)
        questions = json_response["results"]
        #
        context['question_quantity']= len(questions)        
        
        # get the user's selections from request.POST
        user_selections = request.POST

        # create an object to instantiate the function that calculates the result
        result = calculate_result(request, questions, user_selections)        

        if result:
            #
            context['result']= result
            # pass the result for each question to the results template 
            # use HttpResponseRedirect instead of HttpResponse;
            # HttpResponseRedirect takes the URL to which the user will be redirected as an argument
            # Always return an HttpResponseRedirect after successfully
            # dealing with POST data. This prevents data from being
            # posted twice if a user hits the Back button.
            # use reverse function to take the name of the view and return the str value that represents the actual url            
            # include the number of questions in the argument passed to results so that the score has a denominator
            return HttpResponseRedirect(reverse('Education:results', kwargs={'result':result, 'question_quantity':context['question_quantity']}))        
        
        else:
            # ensure that if there's an issue with calculating the result, the view will return a valid response
            # to resolve ValueError- The view Education.views.selection didn't return an HttpResponse object. It returned None instead
            context['error_message'] = "The result was not calculated."
            return render(request, 'edu_quiz/edu_detail.html', context)
                                       
    # display an error message on the detail template if its an invalid request 
    else:
        context = {'error_message': "The request method is invalid.",
                   'questions': None,
                   'mixed_choices': None,
                   'result': None,
                   'question_quantity': None
                   }
        return render(request, 'edu_quiz/edu_detail.html', context)