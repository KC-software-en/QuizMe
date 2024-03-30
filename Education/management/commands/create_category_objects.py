# https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/#module-django.core.management
from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser

# import models
from ...models import Mythology, History, Science_and_Nature 

# import the utility functions used within the create_subcategory_object()
from ...utils import get_specific_json_category, mix_choices

# import html to handle potential HTML entities and aid rendering for create_subcategory_object
import html

# import apps
from django.apps import apps

# When populating the postgresql database don't forget to run this command.
# 'python manage.py migrate --run-sync' to sync the migration into postgresql database.
####################################################################################

'''
Define a class Command that extends BaseCommand. It will create an object for the sub-categories of the Education quiz.
It is intended for private use by the project creator, not its users.
'''
# the custom command can be called using `python manage.py create_category_objects 20 Mythology` to populate Mythology
# be sure to place the desired app name in the handle() before calling the command with its corresponding category_id
# `python manage.py create_category_objects 17 "Science & Nature"` to populate Science & Nature
# `python manage.py create_category_objects 23 History` to populate History
class Command(BaseCommand):
    # define a varible that informs one what the command does
    help = 'Populate the database with quiz objects retrieved from an API'

    # define the arguments for object creation
    # https://docs.python.org/3/library/argparse.html#module-argparse
    def add_arguments(self, parser: CommandParser):
        # add positional arguments        
        parser.add_argument('category_id', type=int, help='The category_id for the desired quiz subcategory')
        parser.add_argument('category_name', type=str, help='The category_name for the desired quiz subcategory')        

    # create an object for the sub-category (e.g.mythology) quiz data
    def handle(self, *args: Any, **options):        
        category_id = options['category_id']
        category_name = options['category_name']

        # call the get_specific_json_category function to get the data for the mythology category
        json_response = get_specific_json_category(quantity=50, category=category_id)
        if json_response == None: 
            self.stderr.write(self.style.ERROR("Failed to retrieve data from the API."))

        # check if there are questions
        if json_response:        
            # save json response as a variable to pass into template
            questions = json_response["results"]
            
            if not questions: 
                self.stderr.write(self.style.WARNING("No questions found in the API response."))        

            # check if question retrieval was successful
            if questions:            
                # find the length of the list of questions 
                total_questions = len(questions)

                # Initialise model with a default value 
                model = None

                # iterate over each question in the results dictionary 
                # enumerate each question to aid the details of the output progress message
                for idx, question in enumerate(questions, start=1):                
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

                    # replace spaces and '&' in the event category names have spaces to create a valid model name                    
                    model_name = category_name.replace(" ", "_").replace("&", "and")                        

                    # use a try-except block to locate the model for the category_name 
                    # retrieve the model dynamically using the app label 'Education' and the constructed model name
                    # this allows model fetching by its name without needing to import it directly
                    try:
                        model = apps.get_model(app_label='Education', model_name=model_name)
                    
                    # raise an error if the model is not found
                    except LookupError:
                        self.stderr.write(self.style.ERROR(f"Cannot locate the model for the selected category: {category_name}."))                                

                    # check that a model was found
                    if model != None: ##                        
                        # create a question object with the above data
                        # this will show on the admin site with the models created for questions & choices
                        question_object = model.objects.create(question = question_text, choices = mixed_choices, correct_answer = correct_choice['choice']) # index choice from the loop above

                        # save the object to the database
                        question_object.save()

                        # Output progress message
                        # use standard output stream (which is where regular output is written)
                        # - instead of directly printing to these streams, allowing for better testing and consistency
                        self.stdout.write(f"Created quiz object {idx} out of {total_questions} for category_id:{category_id}")

                # Output final success message
                # When using management commands & want console output, write to self.stdout and self.stderr,
                # - instead of printing to stdout and stderr directly. Thus it's easier to test a custom command
                # apply styling to console output for the success message (typically highlights the message in green)                   
                self.stdout.write(self.style.SUCCESS(f"Successfully created {total_questions} quiz objects for category_id: {category_id}"))