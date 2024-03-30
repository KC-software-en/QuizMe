# import render to render an HTML template with a given context and return an HttpResponse object
# use get_object_or_404 in views.py to render a HTTP 404 error if a question with the requested ID doesn’t exist
from django.shortcuts import get_object_or_404, render

# imported HttpResponseRedirect 
from django.http import HttpResponseRedirect

# imported reverse
from django.urls import reverse

# import functions from utils.py called in views
from .utils import get_json_categories, get_next_question_id, get_category_names, category_objects

# import all models
from .models import *

# import ast safely evaluate strings containing Python literal structures e.g.strings, lists, dicts
# use to convert str into list
import ast 

# import apps to dynamically fetch a model in detail() & selection() view
from django.apps import apps

#######################################################################################
#######################################################################################

# Create your views here.

# display the category of the General Knowledge quiz
# https://www.youtube.com/watch?v=sgEhb50YSTE
# get json reponse for trivia categories from open trivia db
# index category from the dictionary id
def index_gen(request):
    """A view for the home page of the General Knowledge quiz.

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :return: Return the gen_quiz template
    :rtype: HttpResponse
    """
    # if a user prematurely leaves a quiz & does not use the exit button,
    # - delete the result & session data of the current quiz 
    # - this is done for all the templates the navbar displays
    if 'quiz_result' in request.session:
        del request.session['quiz_result']
        
    # call the categories function & save its response in an assigned variable - NameError if you don't assign it
    response = get_json_categories()
            
    # call the function to return the chosen categories to present a quiz for on the homepage
    category_names = get_category_names(response)       

    # iterate over the list of category_names to return the context for each subcategory in General_Knowledge app
    for category_name in category_names:
        # call the function to retrieve the objects from the django database - viewable on admin site
        question_selection =  category_objects(request, category_name)           
        
        # retrieve question_selection_pks from the session (from utils.category_objects)
        # because the 1st pk needs to be indexed for the 1st question rendered
        # question_selection.first().id chose the 1st question numerically in the database, not the 1st from the randomised list
        question_selection_pks = request.session['question_selection_ids']        
        print(f"index_gen=question_selection_ids in session:{question_selection_pks}") ##     
    
        # the response is the dictionary for trivia categories
        # pass all the context variables into a single dictionary to render in the template correctly
        context = {'category_names': category_names,                                  
                   'question_selection': question_selection,
                   'first_question_id': question_selection_pks[0]
                   }            
        print(f"context:{context}") ##
        
        # render the context to the homepage of General_Knowledge
        return render(request, 'gen_quiz/gen_quiz.html', context) 

# write a view for the quiz question, incl the argument question_id
# question_id is the specific identifier passed in the URL when accessing this view
# it uniquely identifies and retrieves the specific question to display
# Django automatically adds an id field as the primary key for each model (i.e. question.id)
# display the question text 
# render an HTTP 404 error if a question with the requested ID doesn’t exist
def detail(request, category_name, question_id):  
    """A view that displays the quiz question.

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :param category_name: The name of the category the user selected on the category homepage.
    :type category_name: str
    :param question_id: The pk of the question object
    :type question_id: int
    :return: Return the gen_detail template. 
    :rtype: HttpResponse
    """
    response = get_json_categories()
    category_names = get_category_names(response)  

    # Initialise model with a default value because the conditional checking for model gave 
    # - UnboundLocalError: local variable 'model' referenced before assignment
    model = None

    # check if the category_name is in the list of category_names then locate its model    
    if category_name in category_names:
        # use the category_name selected on gen_quiz.html to determine the model to get questions from
        # replace spaces and '&' in the event category names have spaces to create a valid model name
        model_name = category_name.replace(" ", "_").replace("&", "and")
        print(f"Model Name: {model_name}") ##

        # use a try-except block to dynamically find a model that matches the category name
        # - dynamically:instead of explicitly specifying a fixed model in the code, 
        # - generate or determine the model to use at runtime based on certain conditions/data        
        # use apps module to access the get_model function & find the model name         
        try:            
            model = apps.get_model('General_Knowledge', model_name)                        

        # render the detail template displaying the error when a model for a category_name cannot be located
        except LookupError as e:
            error_message = f"{e}"
            context = {'question': None,
                        'choices':None,
                        'category_name': category_name,
                        'error': error_message,
                        'model_exists': False  # Flag indicating whether a model exists for the template to prevent selection() exec
                        }
            print(f"context:{context}")
            return render(request, 'gen_quiz/gen_detail.html', context)    
    
    # check that a model was found
    if model != None: 
        # get the question object associated with a specific question_id in the database
        question = get_object_or_404(model, pk=question_id)    
        print(f"\n\nquestion:{question}")
        print(f"correct_answer:{question.correct_answer}")
    
        # use the helper function literal_eval of the ast module to convert the str representation of the choices list
        # - in the textfield of the category model into a list
        # https://python.readthedocs.io/en/latest/library/ast.html#ast.literal_eval
        # note:ast.literal_eval is safer than eval. it only evaluates literals & not arbitrary expressions, 
        # - reducing the risk of code injection
        # use in template to iterate over the list of choices dictionaries and access the values for the 'choice' key
        convert_choices_textfield_into_list = ast.literal_eval(question.choices)    
    
        # render the gen_detail template & pass the 10 questions, their ids & category as context 
        context = {'question': question,
                   'choices':convert_choices_textfield_into_list,
                   'category_name': category_name 
                   }
        print(f"context:{context}") ##

        # render the context to the detail template of General_Knowledge
        return render(request, 'gen_quiz/gen_detail.html', context)

# create a view that displays the quiz result 
def results(request, category_name): 
    """A view that displays the quiz result.

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :param category_name: The name of the category the user selected on the category homepage.
    :type category_name: str
    :return: Return the gen_result template. 
    :rtype: HttpResponse
    """
    # get the quiz result for the session
    result = request.session.get('quiz_result')
           
    # render the result template  
    # pass the quiz result for the session as a context variable
    context = {'result':result,
               'category_name': category_name
               }   
    
    # render the context to the result template of General_Knowledge
    return render(request, 'gen_quiz/gen_result.html', context)

'''
Write a selection view that handles the submission of form data, goes to the next question and redirects to the results view."
'''
# write a view to answer a question, incl the argument category_name & question_id
# it handles the submitted data
def selection(request, category_name, question_id):   
    """A a selection view that handles the submission of form data, goes to the next question and redirects to the results view. 
    Otherwise the form will be redisplayed.

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :param category_name: The name of the category the user selected on the category homepage.
    :type category_name: str
    :param question_id: The pk of the question object the user has submitted
    :type question_id: int
    :return: Return the gen_detail or the gen_result template. 
    :rtype: HttpResponse
    """  
    # pk refers to the primary key field of a database table
    # django automatically creates a primary key for each model
    response = get_json_categories()
    category_names = get_category_names(response)

    # Initialise model with a default value because the conditional checking for model gave 
    # - UnboundLocalError: local variable 'model' referenced before assignment
    model = None

    # check if the category_name is in the list of category_names then locate its model       
    if category_name in category_names:
        # use the category_name selected on edu_quiz.html to determine the model to get questions from
        # replace spaces and '&' in the event category names have spaces to create a valid model name
        model_name = category_name.replace(" ", "_").replace("&", "and")

        # dynamically find a model that matches the category name
        # - dynamically:instead of explicitly specifying a fixed model in the code, 
        # - generate or determine the model to use at runtime based on certain conditions/data                 
        # use apps module to access the get_model function & find the model name         
        model = apps.get_model('General_Knowledge', model_name)            
        print(f"model:{model}")                                
                                            
    # else print an error for a missing category_name
    else:
        print(f"{category_name} is not in this list: {category_names}")  
    
    # check that a model was found
    if model != None:    
        # get the question object associated with a specific question_id in the database
        question = get_object_or_404(model, pk=question_id)
        #    
        print(f"correct_answer:{question.correct_answer}") ##
    
        # use the helper function literal_eval of the ast module to convert the str representation of the choices list
        # - in the textfield of the category model into a list
        # https://python.readthedocs.io/en/latest/library/ast.html#ast.literal_eval
        # note:ast.literal_eval is safer than eval. it only evaluates literals & not arbitrary expressions, 
        # - reducing the risk of code injection
        # use in template to iterate over the list of choices dictionaries and access the values for the 'choice' key
        convert_choices_textfield_into_list = ast.literal_eval(question.choices)             
            
        # access submitted data by key name with a dictionary-like object- request.POST
        # use the key name 'choice' (defined in gen_detail form input) which returns the ID of the selected choice
        # retrieve the selected choice instance from the database based on the primary key
        # - obtained from the 'choice' key in the submitted form data (request.POST)
        # assumes that the 'id' attribute of the choice in the model is an integer
        try:
            selected_choice = model.objects.get(
                pk=request.POST['choice']
                )
            
        # raise a KeyError if the ID of the choice isn’t found
        # an error occurs if the mapping (dictionary) key was not located in the set of existing keys
        except (KeyError, model.DoesNotExist):        
            # Redisplay the question voting form
            return render(request, 'gen_quiz/gen_detail.html', {
                'category_name': category_name,
                'question': question,
                'choices': convert_choices_textfield_into_list,
                'error_message': "You didn't select a choice."
                })
        
        # use else instead of finally because the selection view for submitting without a choice selection won't render
        else:
            # retrieve the quiz result of the session
            # or let it initialise to 0 in the event its the 1st question
            result = request.session.get('quiz_result', 0)
            
            # iterate over the list of dictionaries for choices and compare the 'id' values
            # check that the id of the selected_choice and the id of the current choice_dict is equal
            # - & that the id in the choice_dict is 1                       
            # (in utils.py the id for the correct answer is 1)
            # else add the point for a correct choice & save the choice        
            for choice_dict in convert_choices_textfield_into_list:
                if selected_choice.id == choice_dict['id'] and choice_dict['id'] == 1: 
                    result += 1
                    selected_choice.save()
                    
            # store the calculated result in the session
            request.session['quiz_result'] = result
                        
            # retrieve question_selection_pks from the session (from utils.category_objects)
            question_selection_pks = request.session['question_selection_ids']        
            print(f"question_selection_ids in session:{question_selection_pks}") ##
    
            # get the next question
            next_question = get_next_question_id(category_name, question_id, question_selection_pks)
            print(f"next_question:{next_question}") ##
    
            # if there is another question available from the question_selection redirect to the detail view again
            # - to display that question 
            # args was used because the urls have positional arguments to pass i.e <str><int>
            if next_question is not None:
                return HttpResponseRedirect(
                    reverse('General_Knowledge:gen_detail', args=(category_name, next_question))
                    )
    
            else:
                # use HttpResponseRedirect instead of HttpResponse;
                # HttpResponseRedirect takes the URL to which the user will be redirected as an argument
                # Always return an HttpResponseRedirect after successfully
                # dealing with POST data. This prevents data from being
                # posted twice if a user hits the Back button.
                # use reverse function to take the name of the view and return the str value that represents the actual url                        
                # args was used because the urls have positional arguments to pass i.e <str>
                # put a comma after category_name since its a str & needs to be treated as a tuple by args 
                # - resolves NoReverseMatch error
                return HttpResponseRedirect(
                    reverse('General_Knowledge:results', args=(category_name,))
                    )

# start new quiz function
def try_new_quiz(request):
    """A view that clears the session data and redirects to the homepage of the category.

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :return: Return the gen_quiz template
    :rtype: HttpResponse    
    """
    # delete the result & session data of the current quiz before starting a new quiz
    if 'quiz_result' in request.session:
        del request.session['quiz_result']

    # render the template for the home page of General_Knowledge      
    return HttpResponseRedirect(
                reverse('General_Knowledge:index_gen')
                )  
        

