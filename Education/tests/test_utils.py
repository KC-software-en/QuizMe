# import unittest on its own to include in class argument
import unittest

#  import unittest to write tests that are not necessarily tied to Django and can be used in any Python project e.g. get API response from open trivia db
from unittest.mock import patch, MagicMock

# import functions in utils.py
from .. import utils

# import random to shuffle choices rendered in the form
import random

##################################################################################################
##################################################################################################

# Create your tests here. Use `py manage.py test Education.tests.test_utils` to run tests in cmd
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
@patch('Education.utils.requests.get')
class TestJsonResponse(unittest.TestCase):
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

# test the mix_choices function
def test_mix_choices_function(self):
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
