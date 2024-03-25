# import models
from .Education.models import Mythology, History, Science_and_Nature 

#
from .Education.utils import get_specific_json_category, mix_choices

# import html to handle potential HTML entities and aid rendering for create_subcategory_object
import html

####################################################################################

'''
Create a function that will create an object for the sub-categories of the Education quiz.
The function & its test is called in Django shell so it is commented out.
'''
# create an object for the sub-category (e.g.mythology) quiz data
# in django shell import the util functions needed for the creation of the obj then call the obj
# place the category id from the quiz_categories.json file as the argument for the function (e.g. 20)
# In project directory cmd: `python manage.py shell`, 
# `from Education.utils import get_specific_json_category, mix_choices, create_subcategory_object`
# `create_subcategory_object(20)`, then `exit()`
# this will populate the sub-category (e.g. mythology) table on the admin site with the quiz data

def create_subcategory_object(category_id, model_name):   
    # call the get_specific_json_category function to get the data for the mythology category
    json_response = get_specific_json_category(quantity=50, category=category_id)
    
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
                question_object = model_name.objects.create(question = question_text, choices = mixed_choices, correct_answer = correct_choice['choice']) # index choice from the loop above
    
                # save the object to the database
                question_object.save()
