# import requests to use the API for edu quiz
import requests

# import html to handle potential HTML entities and aid rendering for create_subcategory_object
import html

# import random to shuffle questions & choices rendered in the form
import random

# import json to work with the data retrieved from the open trivia db API
import json

# import models
from Entertainment.models import *

# import apps to dynamically fetch a model in category_objects() for the detail() view
from django.apps import apps      

# import Http404 to raise an error message if a model is not located in category_objects()
from django.http import Http404

#######################################################################################
#######################################################################################

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
    

# define a function that returns the json response for Open Trivia DB when requesting a specific category
def get_specific_json_category(quantity: int, category: int):
    '''
        Create a function that returns the json response for a specific category on Open Trivia DB.
    '''
    api_url = f"https://opentdb.com/api.php?amount={quantity}&category={category}"
    response = requests.get(api_url)
    
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
    '''
        Create a function that will mix the choices for each question in a quiz.
    '''    
    random.shuffle(choices)
    return choices

# create an object for the sub-category (e.g.mythology) quiz data
# in django shell import the util functions needed for the creation of the obj then call the obj
# place the category id from the quiz_categories.json file as the argument for the function (e.g. 20)
# In project directory cmd: `python manage.py shell`, 
# `from Entertainment.utils import get_specific_json_category, mix_choices, create_subcategory_object`
# `create_mythology_object(20)`, then `exit()`
# this will populate the sub-category (e.g. mythology) table on the admin site with the quiz data
'''
def create_subcategory_object(category):   
    # call the get_specific_json_category function to get the data for the mythology category
    json_response = get_specific_json_category(quantity=50, category=category)
    
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
                question_text = html.unescape(question["question"]) 
                            
                # iterate over the incorrect answers with html.unescape and place them into a list with list comprehension                
                # use html.unescape & handle potential HTML entities for accurate rendering of templates
                # place the answers from the response in a variable 
                # - index it from the list of key:value pairs available for each question(result)
                incorrect_answers = [html.unescape(answer) for answer in question["incorrect_answers"]]             
                # use html.unescape for the correct answer
                correct_answer = html.unescape(question["correct_answer"])                                
                # append the correct answer to the list of choices
                # slice the incorrect_answers & extend it to the choices list - prevents nested lists                               
                choice_texts = []
                choice_texts.append(correct_answer)
                choice_texts.extend(incorrect_answers[:])                                
    
                # initialise an empty list to append the dictionaries containing an id for each choice
                # - else the list will be overwritten each loop, only saving the last dictionary iterated over
                # enumerate each choice to assign an id
                # note: since correct_answer was appended at the start, the id will be 1
                choices_dict = []
                for i, choice in enumerate(choice_texts, start=1):
                    choices_dict.append({'choice': choice, 'id': i})                

                # call the function to rearrange choices and make the extended choice list the argument
                mixed_choices = mix_choices(choices_dict)            
    
                # save the mixed choices to each question in the results dictionary        
                # add a key-value pair to the question dictionary (from the category json response)
                question['mixed_choices'] = mixed_choices
    
                # find the correct answer in mixed_choices
                correct_choice = None
                for choice in mixed_choices:
                    if choice['id'] == 1:
                        correct_choice = choice
                        break
                    
                # create a question object with the above data
                # this will show on the admin site with the models created for questions & choices
                question_object = Science_and_Nature.objects.create(question = question_text, choices = mixed_choices, correct_answer = correct_choice['choice']) # index choice from the loop above
    
                # save the object to the database
                question_object.save()
'''

# create an object for the mythology quiz data
# in django shell import the util functions needed for the creation of the obj then call the obj
# In project directory cmd: `python manage.py shell`, 
# `from Entertainment.utils import get_specific_json_category, mix_choices, create_Video_games_object`
# `from Entertainment.utils import get_specific_json_category, mix_choices, create_History_object`
# `create_Video_games_object()`, then `exit()`
# this will populate the mythology table on the admin site with the quiz data
def create_Video_games_object():   
    '''
        Create a function that will create an object for the sub-categories of the Entertainment quiz.
    '''
    # call the get_specific_json_category function to get the data for the mythology category
    json_response = get_specific_json_category(quantity=50, category=15)
    
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
                question_text = html.unescape(question["question"]) 
                            
                # iterate over the incorrect answers with html.unescape and place them into a list with list comprehension                
                # use html.unescape & handle potential HTML entities for accurate rendering of templates
                # place the answers from the response in a variable 
                # - index it from the list of key:value pairs available for each question(result)
                incorrect_answers = [html.unescape(answer) for answer in question["incorrect_answers"]]             
                # use html.unescape for the correct answer
                correct_answer = html.unescape(question["correct_answer"])                                
                # append the correct answer to the list of choices
                # slice the incorrect_answers & extend it to the choices list - prevents nested lists                               
                choice_texts = []
                choice_texts.append(correct_answer)
                choice_texts.extend(incorrect_answers[:])                                
    
                # initialise an empty list to append the dictionaries containing an id for each choice
                # - else the list will be overwritten each loop, only saving the last dictionary iterated over
                # enumerate each choice to assign an id
                # note: since correct_answer was appended at the start, the id will be 1
                choices_dict = []
                for i, choice in enumerate(choice_texts, start=1):
                    choices_dict.append({'choice': choice, 'id': i})                

                # call the function to rearrange choices and make the extended choice list the argument
                mixed_choices = mix_choices(choices_dict)            
    
                # save the mixed choices to each question in the results dictionary        
                # add a key-value pair to the question dictionary (from the category json response)
                question['mixed_choices'] = mixed_choices
    
                # find the correct answer in mixed_choices
                correct_choice = None
                for choice in mixed_choices:
                    if choice['id'] == 1:
                        correct_choice = choice
                        break
                    
                # create a question object with the above data
                # this will show on the admin site with the models created for questions & choices
                question_object = Video_games.objects.create(question = question_text, choices = mixed_choices, correct_answer = correct_choice['choice']) # index choice from the loop above
    
                # save the object to the database
                question_object.save()


# define a function that returns the django pk for the next question in the quiz
def get_next_question_id(category_name, question_id, question_selection_pks):
    '''
        Create a function that finds the question id for the next question in the quiz.
    '''
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
           else:
               return None


# define a function that will retrieve category names based on the category id for it in the json response
def get_category_names(response):
    '''
        Create a function that finds the question id for the next question in the quiz.
    '''
    # Get the trivia categories values from the dictionary provided in the JSON response
    # Place an empty list as the default argument if the key is not found - this avoids errors in subsequent code
    trivia_categories = response.get("trivia_categories", [])

    # specify the id of the categories to include in the Entertainment app's quizzes
    selected_category_id = [12, 11, 15]

    # collect the categories based on selected_category_id
    selected_categories = [category for category in trivia_categories if category.get("id") in selected_category_id]    
    print(f"selected_categories:{selected_categories}")

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
            # use this to get music only and remove entertainment.
            new_value = category['name'].split(':')[1].strip()
            # Update the dictionary with the new value
            category['name'] = new_value
                        
            print(f"selected_category:{selected_category}")       
            
            # get the name of the category if the id exists for the selected category
            # append each category name to a list
            if selected_category:
                category_name = selected_category.get("name")
                category_names.append(category_name) 

    # return the list of category_names
    return category_names


# define a function that returns the queryset for 10 random objects from the database for each category 
# https://stackoverflow.com/questions/27270958/patch-multiple-methods-from-different-modules-using-python-mock#:~:text=The%20short%20answer%20is%20no%20you%20cannot%20use,one%20of%20the%20time%20by%20single%20patch%20calls.
def category_objects(request, category_name):   
    '''
        A function that retrieves the category queryset from the database based on its category name.
    '''   
    # use the category_name selected on edu_quiz.html to determine the model to get questions from
    # replace spaces and '&' in the event category names have spaces to create a valid model name
    model_name = category_name.replace(" ", "_").replace("&", "and") 
    print('model name : ', model_name)   

    # use a try-except block to find a model that matches the category name
    # use globals()[model_name], it directly accesses the global namespace and doesn't rely on the apps registry. 
    # this approach was more flexible than apps.get_model module since the model name was modified when replacing '&' 
    # - this is not directly compatible with how models are stored in the apps registry
    # the apps module worked to dynamically retrieve a model when only ' ' was being replaced
    # - dynamically:instead of explicitly specifying a fixed model in the code, generate or determine the model to use at runtime based on certain conditions/data
    # use the globals() function to access the global symbol table in Python & retrieve the model with the model name as a key
    # - Note: it relies on the fact that the model class is in the global namespace
    try:        
        model = globals()[model_name]
        print('model name globals: ', model) 
        
    # raise an error if the model is not found
    except LookupError:
        raise Http404("Cannot locate the model for the selected category.")

    # get the 50 questions for the specific category
    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-all-objects    
    all_questions = model.objects.all()

    # create a list containing the pk for each obj
    category_question_ids = [question.id for question in all_questions]

    # get the ids for the selection of 10 questions
    # use random to select 10 questions
    # https://docs.python.org/3.7/library/random.html?highlight=random#random.sample
    # note: random.sample requires a list as its first argument
    question_selection_ids = random.sample(category_question_ids, 10)
    
    # save the question_selection in a session then it will be accessible in selection view as well
    # https://stackoverflow.com/questions/59776172/how-to-pass-querysets-or-the-context-dictronary-from-one-view-to-another-view
    request.session['question_selection_ids'] = question_selection_ids
    
    # filter the objects based on question_selection_ids
    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#the-pk-lookup-shortcut
    question_selection = model.objects.filter(pk__in=question_selection_ids)        

    # return the selected 10 questions from thr database
    return question_selection