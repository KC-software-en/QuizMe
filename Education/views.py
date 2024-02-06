# import render to render an HTML template with a given context and return an HttpResponse object
from multiprocessing import context
from unittest import result
from django.shortcuts import render

# import html to handle potential HTML entities and aid rendering
import html

# Import the login required decorator to prevent unaouthorised access to cetrain views.
from django.contrib.auth.decorators import login_required

# import HttpResponseRedirect
from django.http import HttpResponseRedirect

# import reverse
from django.urls import reverse

# import get_json_categories for the index_edu view
from .utils import get_json_categories, get_specific_json_category, mix_choices

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
    print(f"context:{context}")
    return render(request, 'edu_quiz/edu_quiz.html', context) 

############### %%%%%%%%%%%%%%%%%%%%%%%%%%%% #########################

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