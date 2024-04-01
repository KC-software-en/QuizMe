# import requests to use the API for edu quiz
import requests

# import random to shuffle questions & choices rendered in the form
import random

# import json to work with the data retrieved from the open trivia db API
import json     

# import models
from .models import Mythology, History, Science_and_Nature      

# import apps to dynamically fetch a model in category_objects()
from django.apps import apps

#######################################################################################
#######################################################################################

# define a function that returns the json response for Open Trivia DB
def get_json_categories():
    """Return the json response for the available categories on Open Trivia DB.

    :return: The json response
    :rtype: dict or None
    """
    # get Category Lookup url
    category_lookup = 'https://opentdb.com/api_category.php'
    
    # store url in a variable as a json response
    response = requests.get(category_lookup)
    
    # check if the get request was successful
    # parse the JSON content of the response using the .json() method
    if response.status_code == 200:
        json_response = response.json()
    
        # write Categories to a json file
        # use an indent to ensure each category prints on separate lines
        with open("quiz_categories.json", "w") as f:
            json.dump(json_response, f, indent=4)

        # return the JSON content 
        return json_response
    
    # check if the get request was unsuccessful
    else:
        # print error if unsuccessful request
        # return None to signal that there's no valid data to work with
        error_message = f"Unable to retrieve the specific category - Status code:{response.status_code}"
        print(error_message)
        return None
    
# define a function that returns the json response for Open Trivia DB when requesting a specific category
# create a varible to store the API url for the myth quizzes
# use an f-str to pass in the parameter for quantity
# -> place {} around 5 in the url then replace '5' with 'quantity'
# then place {} around the category id (from quiz_cat.json) for myth & replace '20' with 'category'
# return a list
def get_specific_json_category(quantity: int, category: int):
    """Return the json response for a specific Open Trivia DB quiz category

    :param quantity: Enter the number of questions the API should return
    :type quantity: int
    :param category: Enter the id for the desired quiz category
    :type category: int
    :return: The json response
    :rtype: dict or None
    """
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

        # return the JSON content 
        return json_response

    # check if the get request was unsuccessful
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
    """Mix the choices for each question in a quiz

    :param choices: The choices are a list of 4 options.
    :type choices: list
    :return: Return the shuffled choices
    :rtype: list
    """
    random.shuffle(choices)
    return choices

# define a function that returns the django pk for the next question in the quiz
def get_next_question_id(category_name, question_id, question_selection_pks):
    """Find the question id for the next question in the quiz.

    :param category_name: The name of the subcategory the user selected on the category homepage.
    :type category_name: str
    :param question_id: The primary key for the current question object
    :type question_id: int
    :param question_selection_pks: The list of 10 random primary keys chosen for the quiz session
    :type question_selection_pks: list
    :return: Return the primary key of the next question object, should there be another in the list
    :rtype: int or None
    """
    # iterate over the list of question ids in question_selection_ids from utils.category_objects()
    # - to check if the id generated by django matches the question_id parameter in the url  
    # - & display the specific question that matches the question_id in the URL
    # question_pk refers to the automatically generated primary key (id) of each question in question_selection, 
    # and question_id is the identifier passed in the URL
    # use enumerate to give each question in the selection an idx                    
    for i, question_pk in enumerate(question_selection_pks, start=1):                        
        if question_pk == question_id:
           # save i to a variable. previously it wasn't being preserved properly for the last question
           # - giving an idx out of range error
           # so use the variable instead of i to index the next pk
           # previously i represented the index of the current iteration in the conditional with len,
           # - which may be different from the desired index for the next question's primary key
           next_idx_for_pk = i
           
           # return the next question if its idx is less than / equal to the length of question_selection
           if next_idx_for_pk < len(question_selection_pks):               
               return question_selection_pks[next_idx_for_pk]
           
           # else return None for the last pk in the list
           else:
               return None

# define a function that will retrieve category names based on the category id for it in the json response
def get_category_names(response):
    """Retrieve the desired category names from the Open Trivia DB json response.

    :param response: The json response containing all categories available on Open Trivia DB.
    :type response: dict
    :return: Return the list of selected subcategories for the category according to the ids.
    :rtype: list
    """
    # Get the trivia categories values from the dictionary provided in the JSON response
    # Place an empty list as the default argument if the key is not found - this avoids errors in subsequent code
    trivia_categories = response.get("trivia_categories",[])

    # specify the id of the categories to include in the Education app's quizzes
    selected_category_id = [20, 17, 23] 

    # collect the categories based on selected_category_id
    selected_categories = [category for category in trivia_categories if category.get("id") in selected_category_id]        

    # initialise a variable for the chosen category from the json response
    selected_category = None

    # create an empty list for the category names
    category_names =[]

    # iterate over trivia categories to find the category id specified 
    for category in selected_categories:
        # check if the id in selected_category_id is in the trivia_categories
        if category.get("id") in selected_category_id:
            # assign the current category to the selected_category variable
            selected_category = category                  
            
            # get the name of the category if the id exists for the selected category
            # append each category name to a list
            if selected_category:
                category_name = selected_category.get("name")
                category_names.append(category_name) 

    # return the list of category_names
    return category_names

# define a function that returns the queryset for 10 random objects from the database for each category 
def category_objects(request, category_name):    
    """Retrieve the category queryset from the database based on its category name.

    :param request: The HTTP request object containing information about the client's request.
    :type request: HttpRequest
    :param category_name: The user's selected category
    :type category_name: str    
    :return: The 10 random question objects selected from the database
    :rtype: question_selection or None
    """
    # Initialise model with a default value because the conditional checking for model gave 
    # - UnboundLocalError: local variable 'model' referenced before assignment
    model = None  
               
    # use the category_name selected on edu_quiz.html to determine the model to get questions from
    # replace spaces and '&' in the event category names have spaces to create a valid model name
    model_name = category_name.replace(" ", "_").replace("&", "and")
    
    # use a try-except block to dynamically find a model that matches the category name
    # - dynamically:instead of explicitly specifying a fixed model in the code, 
    # - generate or determine the model to use at runtime based on certain conditions/data        
    # use apps module to access the get_model function & find the model name with its app namespace                
    try:            
        model = apps.get_model('Education', model_name)                        

    # print the error when a model for a category_name cannot be located
    except LookupError as e:
        error_message = f"{e}"
        print(f"error_message:{error_message}")        

    if model != None:
        # get the 50 questions for the specific category with objects.all() ¹
        # https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-all-objects    
        all_questions = model.objects.all()    

        # create a list containing the pk for each obj
        category_question_ids = [question.id for question in all_questions]

        # get the ids for the selection of 10 questions
        # use random to select 10 questions
        # https://docs.python.org/3.7/library/random.html?highlight=random#random.sample
        # note: random.sample requires a list as its first argument ²
        question_selection_ids = random.sample(category_question_ids, 10)

        # save the question_selection in a session then it will be accessible in selection view as well³
        # https://stackoverflow.com/questions/59776172/how-to-pass-querysets-or-the-context-dictronary-from-one-view-to-another-view
        request.session['question_selection_ids'] = question_selection_ids

        # filter the objects based on question_selection_ids
        # https://docs.djangoproject.com/en/3.2/topics/db/queries/#the-pk-lookup-shortcut ⁴
        question_selection = model.objects.filter(pk__in=question_selection_ids)        

        # return the selected 10 questions from the database
        return question_selection