# import HttpRequest to represent an HTTP request.
from django.http import HttpRequest

#  import unittest to write tests that are not necessarily tied to Django and can be used in any Python project e.g. get API response from open trivia db
from unittest.mock import patch, MagicMock

# import functions in utils.py
from .. import utils

# import models
from ..models import Categories, Subcategories, General_Knowledge

# import random to shuffle choices rendered in the form
import random

# import TestCase
from unittest import TestCase

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
from django.test import TransactionTestCase

# AttributeError: 'HttpRequest' object has no attribute 'session'
# import settings & import_module to address the AttributeError
from importlib import import_module
from django.conf import settings

# import mixer to create objects
from mixer.backend.django import mixer

# import sys & StringIO to test for a print statement in cmd
from io import StringIO
import sys

##################################################################################################
##################################################################################################

# Create your tests here. Use `py manage.py test General_Knowledge.tests.test_utils` to run tests in cmd
# after writing a test, run in cmd & it will say fail. 
# next, go to utils.py and create the independent functions. Then it should pass
# run coverage after tests

'''
Create a class to test the functions that request an API response for categorties on Open Trivia DB.
'''
# https://www.django-rest-framework.org/api-guide/testing/#api-test-cases ######## refer back ###
# use patch class decorator & provide the import path to the requests.get function in views.py
# patch the external get function within the requests module, which is used in the views.get_json_categories function
# - to intercept the HTTP request made by the code and control the response during testing
@patch('General_Knowledge.utils.requests.get')
class TestJsonResponse(TestCase):
    def setUp(self):
        pass
    
    # test successful response for json categories by calling its function from views 
    # https://docs.python.org/3.7/library/unittest.mock.html#the-mock-class
    # mock_get_request is a parameter representing the function that replaces a mock during the test
    # - represents the requests.get function in the patch decorator, which is called inside the get_json_categories function
    def test_get_json_categories_ok(self, mock_get_request):  
        # create an instance of MagicMock & assign it to the response object
        # simulate a successful HTTP response with a status_code attribute
        # reflect that the get_json_categories function calls response.json() by
        # - simulate the expected JSON dictionary by setting a return_value for response.json()
        mock_response_ok = MagicMock()
        mock_response_ok.status_code = 200
        mock_response_ok.json.return_value = {
            "trivia_categories": [
                {"id":1, "name":"category1"}, 
                {"id":2, "name":"category2"}
                ]
        }
        
        # set the return value for response of mock_get as mock_response
        mock_get_request.return_value = mock_response_ok

        # call the function in views.py that internally call the requests.get
        response = utils.get_json_categories()

        # assert that API response was successfully received & not None
        # assert that the type of json_response is a dict (dictionary) - ensure a python dictionary
        # - https://docs.python.org/3.7/library/unittest.html?highlight=assertisinstance#unittest.TestCase.assertIsInstance
        # - in Python, everything is an object, and data types are implemented as classes
        # - dict is the class representing dictionaries in Python
        # assert that the key "trivia_categories" is in the dictionary json_response [a in b where assertIn(a,b)]
        self.assertIsNotNone(response, msg='Should check that an API response was successfully received.')
        self.assertIsInstance(response, dict, msg='Should check that json_response is a dictionary.')
        self.assertIn('trivia_categories', response, msg='Should check that the trivia_categories key is present in the dictionary json_response.')        
    
    # test unsuccessful response for json categories by calling its function from views  
    # https://docs.python.org/3.7/library/unittest.mock.html#the-mock-class
    # mock_get_request is a parameter representing the function that replaces a mock during the test
    # - represents the requests.get function in the patch decorator, which is called inside the get_json_categories function
    def test_get_json_categories_error(self, mock_get_request):  
        # create an instance of MagicMock & assign it to the response object
        # simulate an unsuccessful HTTP response with a status_code attribute        
        mock_response_error = MagicMock()
        mock_response_error.status_code = 429
        mock_response_error.error_message = "Too many requests to the API in a given amount of time ('rate limiting')."
                
        # set the return value for response of mock_get_request as mock_response_error
        mock_get_request.return_value = mock_response_error

        # call the function in views.py that internally call the requests.get
        response_error = utils.get_json_categories()

        # assert that API response was unsuccessful & None        
        self.assertIsNone(response_error, msg='Should check that the categories API response was unsuccessful & returns None.')        

    # test successful response for specific json categories by calling its function from views  
    # mock_get_request is an argument representing the mocked version of the requests.get function specified in the @patch decorator, 
    # - used within the get_specific_json_category function.
    def test_get_specific_json_category_success(self, mock_get_request):
        # set up mock for a successful response
        # create a mock object by instantiating a MagicMock class & assigning it to the response object
        # - it will simulate an HTTP response object
        # - MagicMock allows you to access and set attributes, call methods, etc, without explicitly defining them
        # simulate a successful HTTP response with a status_code attribute
        # reflect that the get_specific_json_category function calls response.json() by
        # - simulate the expected JSON dictionary by setting a return_value for response.json()
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

        # call the function in views.py that internally call the requests.get
        response_ok = utils.get_specific_json_category(quantity=50, category=20)
        
        # assert that API response was successfully received & not None
        # assert that the type of json_response is a dict (dictionary) - ensure a python dictionary                
        # - dict is the class representing dictionaries in Python
        # assert that the key "results" is in the dictionary json_response [a in b where assertIn(a,b)]
        self.assertIsNotNone(response_ok, msg='Should check that an API response was successfully received.')
        self.assertIsInstance(response_ok, dict, msg='Should check that json_response is a dictionary.')
        self.assertIn('results', response_ok, msg='Should check that the trivia_categories key is present in the dictionary json_response.')        

    # test error response for specific json categories by calling its function from views  
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

        # set the return value for response of mock_get as mock_response
        mock_get_request.return_value = mock_error_response

        # call the function in views.py that internally call the requests.get
        response_error = utils.get_specific_json_category(quantity=50, category=20)
        
        # assert that API response was unsuccessful & returns None        
        self.assertIsNone(response_error, msg='Should check that an API response was unsuccessful & returns None.')        


'''
Create a class that tests the CreateSubcategoryObject function instantiated in the django shell to populate the database for each model.
The test is in a doctstring in test_utils since its run in django shell.

# use TestCase from django.test to start with a fresh database each time
class TestCreateSubcategoryObject(TransactionTestCase):
    # setup an instance of the RequestFactory class since get_specific_json_category uses request
    def setUp(self):    
        self.factory = RequestFactory()

    # test create_subcategory_object
    def test_create_subcategory_object(self):
        with patch('General_Knowledge.views.create_subcategory_object') as mock_create_subcategory_object:
            # set up a successful mock response for the mock_create_subcategory_object function
            mock_object = [
                    {
                    "question":"question{i}",                        
                    "mixed_choices":[{"mixed_choice{i}":"mixed_choice{i}", 
                                        "id{i}":"id{i}"} for i in range(1,5)],
                    "correct_answer":"correct_answer{i}",
                    } for i in range(1,51) # use list comprehension to create 50 mock objects (the last number is ignored)
                ]
                       
            # set the return value for mock_object as mock_response_ok
            mock_create_subcategory_object.return_value = mock_object
            
            # Create a GET request for the view with reverse 
            # use the name defined in urls.py with the arguments passed in the view in view.py
            ##request = self.factory.get(reverse('General_Knowledge:gen_detail', args=[50, 20]))
            ##response = utils.get_specific_json_category(request, quantity=50, category=20)

            # call the create_subcategory_object function to test it with a category id
            utils.create_subcategory_object(20)
            mock_create_subcategory_object.assert_called_once()

            # get the 50 objects created in the database
            category_objects = models.General_Knowledge.objects.all()

            # make assertions about the object
            # assert there are 50 objects for the category 
            # - use range instead of just the int because assertCountEqual compares 2 iterables
            self.assertEqual(category_objects.count(), 50, 
                                  msg='Should check that there are 50 objects for the category in the database.')
            # make assertions for each attribute in the 50 objects
            # iterate over the queryset of category_objects & enumerate with an idx that starts at 1
            for i, category_object in enumerate(category_objects, start=1):
                self.assertEqual(category_object.question, 'question{i}', 
                                 msg='Should check that question{i} is the question attribute for the object.')
                # use "" inside dictionary not ' to avoid json.decoder.JSONDecodeError: 
                # - Expecting property name enclosed in double quotes
                expected_mock_mixed_choices = '[{"mixed_choice{i}":"mixed_choice{i}", "id{i}":"id{i}"}]'
                print(f"expected_mock_mixed_choices:{expected_mock_mixed_choices}")
                actual_choices = str(category_object.choices)
                print(f"actual_choices:{actual_choices}")
                self.assertEqual(actual_choices, expected_mock_mixed_choices,
                                 msg='Should check that the list of mixed choices are in the choices attribute for the object.')
                self.assertEqual(category_object.correct_answer, "correct_answer{i}", 
                                 msg='Should check that correct_answer{i} is an attribute for the object.')
'''

'''
Create a class to test miscellaneous functions in utils.py
'''
# create a class TestVariousUtils
class TestVariousUtils(TestCase):
    # setup 
    def setUp(self):
        pass

    # test the mix_choices function
    def test_mix_choices(self):
        # create a list of choices to test
        # use random to check that it will rearrange the list
        choices = ['Choice1', 'Choice2', 'Choice3']
        random.shuffle(choices) 

        # call the function from views.py to test it
        mixed_choices = utils.mix_choices(choices)

        # assert that the length of the list is the same after shuffling
        # assert that the order of items in the original test list differs from the shuffled choices list
        # assert that both lists contain the same items, regardless of their order
        self.assertEqual(len(choices), 3, msg='Should check that the shuffled choices is the length of original choice list')
        self.assertNotEqual(['Choice1', 'Choice2', 'Choice3'], choices,
                                msg='Should check that the order of items in the original test list differs from the shuffled choices list.')
        self.assertCountEqual(mixed_choices, choices,
                                msg='Should check that the two lists contain the same items, regardless of their order')

    # test get_next_question_id
    # patch the selection view where get_next_question_id was called
    @patch('General_Knowledge.views.selection')
    def test_get_next_question_id(self, mock_question_selection_pks):
        # mock pks of question_selection
        mock_question_selection_pks.return_value = [12, 2, 28, 49, 35, 37, 14, 1, 9, 15]

        # test when there is another pk after current pk
        result = utils.get_next_question_id('category_name', 28, [12, 2, 28, 49, 35, 37, 14, 1, 9, 15])
        self.assertEqual(result, 49, msg='Should check that the next pk in the list is located.')

        # test when there is not another pk after current pk
        result = utils.get_next_question_id('category_name', 15, [12, 2, 28, 49, 35, 37, 14, 1, 9, 15])
        self.assertIsNone(result, msg='Should check that there is not a next pk in the list.')

        # test when the pk is not in the question_selection_pks
        result = utils.get_next_question_id('category_name', 50, [12, 2, 28, 49, 35, 37, 14, 1, 9, 15])
        self.assertIsNone(result, msg='Should check that None is returned for a pk not in the list')

    # test get_category_names that have a name for the corresponding id selection
    def test_get_category_names_found(self):
        # create a MagicMock object to mock the response from the external get_category_names function
        mock_response = MagicMock()
        
        # set up a mock_response containing a dictionary of trivia category lists
        mock_response = {
                        "trivia_categories": [
                            {
                                "id": 9, # 9 is a selected_category_id in utils.py
                                "name": "category1"
                            }
                            ]
                        }
        
        # mock the list of category_names
        # index the dictionary to access the values for "name"                
        mock_category_names = [item["name"] for item in mock_response["trivia_categories"]]        

        # call get_category_names with mock_response
        category_names = utils.get_category_names(mock_response)
        
        # assert that the names are there for the selected category ids
        self.assertEqual(category_names, mock_category_names, msg='Should check that category1 is in the mock_response.')

    # test get_category_names if the category_name is not in the json response
    def test_no_category_name(self):
        # set up a mock_response containing a dictionary of trivia category lists
        # alter the id so that a category_name cannot be found by its id
        mock_response = {
                        "trivia_categories": [
                            {
                                "id": 1, # 20 is a selected_category_id in utils.py so its excluded here
                                "name": "category1"
                            }                            
                            ]
                        }
        # call get_category_names with mock_response
        category_names = utils.get_category_names(mock_response)

        # assert that the name is not there for the selected category id
        self.assertListEqual(category_names, [], msg='Should check that the list is empty if a selected category id is not there.')

"""
Create a class that tests the category_objects function.
"""
# create tests for a valid category_name and an invalid category_name when locating a model to retrieve its category_objects
# use TransactionTestCase because tests for category objects rely on database access 
# - this ensures test objects are not created on the admin site
class TestCategoryObjects(TransactionTestCase):    
    # setup the conditions needed for functions in the class
    def setUp(self):
        # Create an instance of the HttpRequest class
        self.request = HttpRequest()

        # address the AttributeError: 'HttpRequest' object has no attribute 'session' even though it's in settings.py 
        # - (& import SessionMiddleware did not work)
        # - by setting up a new session for the HttpRequest object in the Django application.
        # import the session engine based on the configured SESSION_ENGINE setting in Django
        # - the SESSION_ENGINE setting specifies the storage backend for Django's session framework
        # - create a new session store instance using the imported session engine
        # set session_key to None, indicating that a new session will be created
        # assign the created session store to the session attribute of the HttpRequest object
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        # set up the category instance
        self.category = Categories.objects.create(category="General Knowledge", description="General Knowledge description")

        # set up the category instance
        self.subcategory = Subcategories.objects.create(subcategory = "subcategory1", description="subcategory1 description", category=self.category)

        # set up the 50 random objects retrieved
        self.mock_questions = [General_Knowledge.objects.create(                                       
                                      question=f"question{i}", 
                                      choices = [f'choice{i}' for i in range(1,5)], 
                                      correct_answer = f'choice1',
                                      category = self.category
                                      ) 
                        for i in range(1,51)]
        
        # mock the question_selection_ids as a list of 10 int ids(i.e. pk)
        self.mock_question_selection_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # 10 question objects for the question_selection
        self.mock_question_selection = self.mock_questions[:10]         

    # patch to mock the filter method of the General_Knowledge.objects manager. 
    # - this is done to ensure that when filter is called in the utils.category_objects function, 
    # - it returns the specified self.mock_question_selection instead of actually querying the database.         
    # not a literal file path but rather a string representing the import path of the object to mock. 
    @patch('General_Knowledge.utils.General_Knowledge.objects.filter')        
    def test_category_objects(self, mock_filter):
        # set up the return value for the filtered selection
        mock_filter.return_value = MagicMock(filter=lambda: self.mock_question_selection)        
        
        # mock the count() method of the queryset and make it return the desired count        
        # mock the count method on the queryset returned by filter with the side_effect attribute of the mock object to return the desired value 
        # - for AssertionError: <MagicMock name='filter().count()' id='94005744'> != 10 : Should check that question_selection contains 10 objects
        # use side_effect instead of return_value for AttributeError: 'builtin_function_or_method' object has no attribute 'return_value'
        # https://docs.python.org/3.7/library/unittest.mock.html#the-mock-class
        # - & https://docs.python.org/3.7/library/unittest.mock.html#unittest.mock.Mock.side_effect
        # https://docs.python.org/3.7/library/unittest.mock-examples.html?highlight=lambda#partial-mocking
        mock_filter.return_value.count.side_effect = lambda:10                 

        # set the new dictionary key that stores the mock_question_selection_ids for the session
        self.request.session['mock_question_selection_ids'] = self.mock_question_selection_ids

        # call the category_objects function
        response = utils.category_objects(self.request, 'General Knowledge')

        # assertions
        # assert that the mock_question_selection exists
        # assert that there are 10 objects in the mock_question_selection
        # assert that the mock_question_selection_ids key was set for the session
        self.assertIsNotNone(self.mock_question_selection, msg ='Should check that question_selection is not None.')        
        self.assertEqual(response.count(), 10, msg ='Should check that question_selection contains 10 objects.')  
        self.assertEqual(self.request.session['mock_question_selection_ids'], self.mock_question_selection_ids, 
                         msg='Should check that there are a list of 10 ids.')  # Ensure the session is set correctly

    # test for an error raised if globals does not have a model for a category name
    # dont incl category_objects in path to avoid AttributeError: <function category_objects at 0x0489E2B8> does not have the attribute 'globals'
    @patch('General_Knowledge.views.apps.get_model')
    def test_category_objects_invalid_category(self, mock_get_model):        
        # redirect the standard output (stdout) to the StringIO object captured_output. 
        # - this captures any output that is printed to the standard output during the execution of the category_objects function
        captured_output = StringIO()
        sys.stdout = captured_output

        # mock the globals function to raise a LookupError for an incorrect category_name
        mock_get_model.side_effect = LookupError

        # call the category_objects function
        response = utils.category_objects(self.request, 'Invalid category')

        # reset stdout to restore the standard output stream to its original state after redirecting it for testing purposes
        # - ensures that subsequent code execution within the test/(other tests) are not affected by stdout redirection 
        sys.stdout = sys.__stdout__

        # assert that the response is None when an invalid category is provided
        # assert that the string 'error_message' is present in the captured output.
        self.assertIsNone(response, msg='Should return None for an invalid category.')
        self.assertIn('error_message', captured_output.getvalue(), msg='Should check that the str is present in the stdout for LookupError.')
        