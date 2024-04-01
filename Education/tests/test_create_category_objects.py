
from io import StringIO
import sys
from django.core.management import call_command

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase¹
from django.test import TransactionTestCase

# import classes from models.py 
from ..models import Mythology

# import utils used in command
from ..utils import get_specific_json_category

#  import unittest to write tests that are not necessarily tied to Django and can be used in any Python project e.g. get API response from open trivia db
from unittest.mock import patch, MagicMock, Mock

# import TestCase
from unittest import TestCase

# import apps to dynamically fetch a model 
from django.apps import apps

# NOTE: management commands are automatically discovered when placed within the management/commands directory of an app
# - therefore, you do not need to import create_subcategory_objects explicitly in a test case 
# - Django will find and execute the command when you call it using call_command

##############################################################################################

# Create your tests here. Use `py manage.py test Education.tests.test_create_category_objects` to run tests in cmd
# after writing a test, run in cmd & it will say fail. 
# next, go to create_category_objects.py and create the command. Then it should pass
# run coverage after tests

# use patch class decorator & provide the import path to the requests.get function in views.py
# patch the external get function within the requests module, which is used in the views.get_json_categories function
# - to intercept the HTTP request made by the code and control the response during testing
@patch('Education.utils.requests.get')
class TestGetSpecificJsonCategoryError(TestCase):
    # test error response for specific json categories by calling its function from utils  
    # mock_get_request is an argument representing the mocked version of the requests.get function specified in the @patch decorator, 
    # - used within the get_specific_json_category function.    
    def test_get_specific_json_category_error(self, mock_get_request):
        # set up mock for an unsuccessful response
        # create a mock object by instantiating a MagicMock class & assigning it to the response object
        # - it will simulate an HTTP response object
        # - MagicMock allows you to access and set attributes, call methods, etc, without explicitly defining them
        # simulate an unsuccessful HTTP response with a status_code attribute e.g. 429 for rate limit exceeded        
        # simulate an error message for the mock test
        mock_error_response = MagicMock()        
        mock_error_response.status_code = 429
        mock_error_response.error_message = "Too many requests to the API in a given amount of time ('rate limiting')."

        # set the return value for response of mock_get_request as mock_error_response
        mock_get_request.return_value = mock_error_response

        # redirect stderr into a str
        out = StringIO() 

        # set the variables        
        category_id = 20
        category_name = 'Mythology'        

        # call the command (use the name of the command which is the file name, not Command/handle)
        # cast category_id to str because call_command() expects string arguments
        call_command('create_category_objects', str(category_id), category_name, stderr=out)

        # assertions
        # https://docs.python.org/3.7/library/unittest.html#assert-methods ²
        self.assertIn('Failed to retrieve data from the API', out.getvalue(), 
                      msg='Should check that a str is in the error message for failing to retrieve API response')        

    # test for an empty json response        
    def test_no_questions_in_json(self, mock_get_request):
        # set up mock for an successful API retrieval but an empty json response
        # create a mock object by instantiating a MagicMock class & assigning it to the response object
        # - it will simulate an HTTP response object
        # - MagicMock allows you to access and set attributes, call methods, etc, without explicitly defining them
        # simulate an successful HTTP response with a status_code attribute 
        # simulate an error message for the mock test
        mock_response = MagicMock()        
        mock_response.status_code = 200
        mock_response.json.return_value = {"results":[]}

        # set the return value for response of mock_get_request as mock_response
        mock_get_request.return_value = mock_response

        # redirect stderr into a str
        out = StringIO() 

        # set the variables        
        category_id = 20
        category_name = 'Mythology'        

        # call the command (use the name of the command which is the file name, not Command/handle)
        # cast category_id to str because call_command() expects string arguments
        call_command('create_category_objects', str(category_id), category_name, stderr=out)

        # assertions
        self.assertIn('No questions found in the API response', out.getvalue(), 
                      msg='Should check that a str is in the error message for an empty json response')        

# create a class that tests finding a model.         
@patch('Education.views.apps.get_model')
class TestFindModel(TestCase):
    # create a test that locates a model in the app    
    def test_find_model_success(self, mock_get_model): 
        # create a MagicMock object to mock the behaviour of the Mythology class³
        # use spec=Mythology to ensure that mock_model behaves like an instance of the Mythology class
        # https://docs.python.org/3.7/library/unittest.mock.html#the-mock-class 
        # set the return value of mock_get_model to be the mock_model object
        mock_model = MagicMock(spec=Mythology)     
        mock_get_model.return_value = mock_model
        
        # redirect stderr into a str
        out = StringIO() 

        # set the variables        
        category_id = 20
        category_name = 'Mythology'        

        # call the command (use the name of the command which is the file name, not Command/handle)
        # cast category_id to str because call_command() expects string arguments
        call_command('create_category_objects', str(category_id), category_name, stdout=out)
   
        # assert that the result object is an instance of the same class as mock_model⁴
        # https://docs.python.org/3.7/library/unittest.html?highlight=assertisinstance#unittest.TestCase.assertIsInstance 
        # assert that the result is not none, indicating successful retrieval
        self.assertIsInstance(mock_get_model.return_value, type(mock_model),
                               msg='Should check that the response to the function get_model is a model instance.')
        self.assertIsNotNone(out, msg='Should check that the model is not none.')   

    # test for an error raised if globals does not have a model for a category name    
    def test_find_model_fail(self, mock_get_model):            
        # mock the arguments for the detail() function
        mock_category_name_absent = 'Sports'   
        mock_category_id = 21     

        # mock the get_model function to raise a LookupError for an incorrect category_name (i.e. no corresponding model)                       
        mock_get_model.side_effect = LookupError

        # redirect stderr into a str
        out = StringIO() 

        # call the command (use the name of the command which is the file name, not Command/handle)
        # cast category_id to str because call_command() expects string arguments
        call_command('create_category_objects', str(mock_category_id), mock_category_name_absent, stderr=out)

        # assertions
        self.assertIn('Cannot locate the model for the selected category', out.getvalue(), 
                      msg='Should check that a str is in the error message for a model not found')        

        
                

# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#management-commands
# Management commands can be tested with the call_command() function⁵. 
# The output can be redirected into a StringIO instance
# create a class that tests the command create_subcategory_objects
class TestCreateSubcategoryObjects(TransactionTestCase):
    @patch('Education.utils.requests.get')
    def test_create_subcategory_objects(self, mock_get_request):
        mock_ok_response = MagicMock()
        mock_ok_response.status_code = 200
        mock_ok_response.json.return_value = {
            "results":[
                {"type":"type1",
                 "difficulty":"level",
                 "category":"category1",
                 "question":"question1",
                 "correct_answer":"correct_answer1",
                 "incorrect_answers":[
                     "incorrect_answer",
                     "incorrect_answer2",
                     "incorrect_answer3",                     
                 ]
                 }
            ]
        }

        # set the return value for response of mock_get as mock_response
        mock_get_request.return_value = mock_ok_response

        out = StringIO() 
        ##sys.stdout = out       
        
        # set the variables
        total_questions = 50
        category_id = 20
        category_name = 'Mythology'
        idx = 1

        # call the command (use the name of the command which is the file name, not Command/handle)
        call_command('create_category_objects', category_id, category_name, stdout=out)
        print(f"out:{out.getvalue()}")##

        # set the expected output
        progress_expected_output = f"Created quiz object {idx} out of {total_questions} for category_id:{category_id}"
        final_expected_output = f"Successfully created {total_questions} quiz objects for category_id: {category_id}"
        
        ##sys.stdout = sys.__stdout__

        # assertions
        self.assertIn(progress_expected_output, out.getvalue(), 
                      msg='Should check that a progess message reports the creation of a specific object.')
        self.assertIn(final_expected_output, out.getvalue(), 
                      msg='Should check that a progess message reports the creation of 50 quiz objects.')

class TestCreateSubcategoryObjects2(TransactionTestCase):
    def test_create_subcategory_objects2(self):
        out = StringIO
        call_command('create_category_objects', 20, 'Mythology', stdout=out)
        self.assertIn('Created quiz object', out.getvalue())
        self.assertIn('Successfully created', out.getvalue())
