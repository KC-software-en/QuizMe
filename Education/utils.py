# import requests to use the API for edu quiz
import requests

# import html to handle potential HTML entities and aid rendering
import html

# import random to shuffle questions & choices rendered in the form
import random

# import json to work with the data retrieved from the open trivia db API
import json

# import models
from .models import Mythology

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

'''
Create a function that will mix the choices for each question in a quiz.
'''    
# rearrange the options of answers
# use the random module & its shuffle function to rearrange
# return a list of choices
def mix_choices(choices: list):
    random.shuffle(choices)
    return choices

'''
Create a function that will create an object for the sub-categories of the Education quiz.
'''
# create an object for the sub-category (e.g.mythology) quiz data
# in django shell import the util functions needed for the creation of the obj then call the obj
# place the category id from the json response as the argument for the function (e.g. 20)
# In project directory cmd: `python manage.py shell`, 
# `from Education.utils import get_specific_json_category, mix_choices, create_mythology_object`
# `create_mythology_object(20)`, then `exit()`
# this will populate the sub-category (e.g. mythology) table on the admin site with the quiz data
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
                question_object = Mythology.objects.create(question = question_text, choices = mixed_choices, correct_answer = correct_choice['choice']) # index choice from the loop above
    
                # save the object to the database
                question_object.save()

'''
Create a function that find the question id for the next question in the quiz.
'''
# define a function that returns the django pk for the next question in the quiz
def get_next_question_id(category_name, question_id, question_selection_pks):
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

'''
A function that retrieves the desired category names from the Open Trivia DB json response.
'''
# define a function that will retrieve category names based on the category id for it in the json response
def get_category_names(response):    
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
                return category_name
            
            # exit the loop when the desired category is found            
            break

'''
A function that retrieves the category queryset from the database based on its category name.
'''  
# define a function that returns the queryset for 10 random objects from the database for each category 
def category_objects(request, category_name):    
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