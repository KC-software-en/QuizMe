# import requests to use the API for edu quiz
import requests

# import from urllib to work with URL requests & the response handling process when making HTTP requests
from urllib import request, response

# https://docs.djangoproject.com/en/5.0/intro/tutorial05/#id7
# reverse function is used in Django to generate URLs for views based on their names or patterns
from django.urls import reverse

# import all views
# (had to use this structure so that response object would recognise views)
from .. import views

# import json to work with the data retrieved from the open trivia db API
import json

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
# import RequestFactory to generate a HttpRequest objects & simulate HTTP requests (faster than using Client)
# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#the-test-client
# https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#the-request-factory
# import base class for all Django test cases (for writing tests, including test assertions, database setup and teardown, and other testing infrastructure)
from django.test import TestCase, RequestFactory, Client

# import unittest on its own to include in class argument
import unittest

#  import unittest to write tests that are not necessarily tied to Django and can be used in any Python project e.g. get API response from open trivia db
from unittest.mock import patch, MagicMock

# import AnonymousUser model - a special type of user object representing an unauthenticated user or a user who is not logged in
from django.contrib.auth.models import AnonymousUser

# import logging then comment out after debugging view response to pass assertions
#import logging######

# import TemplateResponse because it is a specialised HttpResponse subclass that is specifically designed for representing responses generated from rendering templates
# use the render function in Django views & it typically returns a TemplateResponse instance
from django.template.response import TemplateResponse  

# import random to shuffle choices rendered in the form
import random



#############################################################################################
#############################################################################################
# Create your tests here. Use `py manage.py test Education.tests.test_views` to run tests in cmd
# after writing a test, run in cmd & it will say fail. 
# next, go to views.py and create the views. Then it should pass
# run coverage after tests

'''
Create a class to test the functions that request an API response for categorties on Open Trivia DB.
'''
# https://www.django-rest-framework.org/api-guide/testing/#api-test-cases ######## refer back ###
# use patch class decorator & provide the import path to the requests.get function in your actual codebase
# patch the external get function within the requests module, which is used in the views.get_json_categories function
# - to intercept the HTTP request made by the code and control the response during testing
@patch('Education.views.requests.get')
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
        response = views.get_json_categories()

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
        response_error = views.get_json_categories()

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
        response_ok = views.get_specific_json_category(quantity=50, category=20)
        
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
        response_error = views.get_specific_json_category(quantity=50, category=20)
        
        # assert that API response was unsuccessful & returns None        
        self.assertIsNone(response_error, msg='Should check that an API response was unsuccessful & returns None.')        

'''
Create a class to test the views rendered in Education.
'''
#
class TestEducationViews(TestCase):
    def setUp(self):
        # create fake requests with a RequestFactory instance - sets up the test environment
        # set up a Django test client for making HTTP requests in the tests
        # setup a user who is not logged in with AnonymousUser
        self.factory = RequestFactory()   
        self.client = Client()     #######
        self.anonymous_user = AnonymousUser()

    def test_index_view(self):
        # create an instance of index view
        # test index view as if it were deployed at /index.html
        request = self.factory.get(reverse('Education:index'))

        # simulate a request to index view and capture the resulting HTTP response
        response = views.index(request)

        # Simulate an anonymous user because Edu is accessible to unauthenticated users
        request.user = self.anonymous_user

        # assert that the HTTP response status code is 200 (OK), indicating a successful request.        
        self.assertEqual(response.status_code, 200, msg='Should check for a successful GET request of index view for anyone')        

    # test the 'index_edu' view with RequestFactory to create a fake GET request
    def test_index_edu_view_with_reqfac(self):
        # create a fake GET request to the 'index_edu' view with a specified category_id 
        # simulate a request to index_edu view and capture the resulting HTTP response
        request = self.factory.get(reverse('Education:index_edu', kwargs={'category_id': 20}))
        request.user = AnonymousUser()

        # simulate a request to index_edu view and capture the resulting HTTP response 
        response = views.index_edu(request.user)

        # assert that the HTTP response status code is 200 (OK), indicating a successful request.        
        # (need request to use status_code)
        self.assertEqual(response.status_code, 200, msg='Should check for a successful GET request of index_edu view for anyone')

    # test the 'index_edu' view using the Django test client
    def test_index_edu_view_with_client(self):    
        # make a GET request to the 'index_edu' view using the Django test client
        response = self.client.get(reverse('Education:index_edu', kwargs={'category_id': 20}))

        # assert that the view renders the edu_quiz template - use path from template directory
        self.assertTemplateUsed(response, 'edu_quiz/edu_quiz.html', msg_prefix='Should check that the edu_quiz template was used')    

    # test the mix_choices function
    def test_mix_choices_function(self):
        # create a list of choices to test
        # use random to check that it will rearrange the list
        choices = ['Choice1', 'Choice2', 'Choice3']
        random.shuffle(choices) 

        # call the function from views.py to test it
        mixed_choices = views.mix_choices(choices)

        # assert that the length of the list is the same after shuffling
        # assert that the order of items in the original test list differs from the shuffled choices list
        # assert that both lists contain the same items, regardless of their order
        self.assertEqual(len(choices), 3, msg='Should check that the shuffled choices is the length of original choice list')
        self.assertNotEqual(['Choice1', 'Choice2', 'Choice3'], choices,
                             msg='Should check that the order of items in the original test list differs from the shuffled choices list.')
        self.assertCountEqual(mixed_choices, choices,
                               msg='Should check that the two lists contain the same items, regardless of their order')

    def test_get_questions_and_choices(self):
        pass
###################################################################################    


class TestGetQuestionsAndChoices(TestCase):
    def setUp(self):
        pass
        

    def test_get_questions_and_choices_success(self):
        # Create a GET request for the view
        request = self.factory.get('/path/to/your/view/50/20/')
        
        # Call the view function with the GET request
        response = views.get_questions_and_choices(request, quantity=50, category=20)

        # Assert that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # add more assertions 

    def test_get_questions_and_choices_no_questions(self):
        # Create a GET request for the view
        request = self.factory.get('/path/to/your/view/50/20/')
        
        # Mock the get_specific_json_category function to return a response without questions
        with patch('Education.views.get_specific_json_category') as mock_get_specific_json:
            mock_get_specific_json.return_value = {'results': []}

            # Call the view function with the GET request
            response = views.get_questions_and_choices(request, quantity=50, category=20)

        # Assert that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # add more assertions 

    # Add more test cases as needed
####################################################################################
'''
possible assertions
    def test_get_questions_view(self):
        response = self.client.get(reverse('get_questions', kwargs={'quantity': 50, 'category': 20}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edu_quiz/edu_detail.html')
        self.assertIn('question_texts', response.context)
        self.assertIsNone(response.context['mixed_choices'])
        self.assertIsNone(response.context['error_message'])

    def test_get_choices_view(self):
        response = self.client.get(reverse('get_choices', kwargs={'category_id': 20}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edu_quiz/edu_detail.html')
        self.assertIsNone(response.context['question_texts'])
        self.assertIn('mixed_choices', response.context)
        self.assertIsNone(response.context['error_message'])
'''

#removed these tests after implementing mock, patch
'''
# https://www.django-rest-framework.org/api-guide/testing/#requestsclient
    def test_get_json_categories_with_unittest(self):  
        # use unittest to simulate an external API request    
        category_lookup = 'https://opentdb.com/api_category.php'        
        response = requests.get(category_lookup)         
        if response.status_code == 200:
            json_response = response.json()                    
                
        # assert that the HTTP response status code is 200 (OK), indicating a successful request.
        # assert that API response was successfully received and parsed into a JSON format
        # assert that the type of json_response is a dict (dictionary) - ensure a python dictionary
        # - https://docs.python.org/3.7/library/unittest.html?highlight=assertisinstance#unittest.TestCase.assertIsInstance
        # - in Python, everything is an object, and data types are implemented as classes
        # - dict is the class representing dictionaries in Python
        # assert that the key "trivia_categories" is in the dictionary json_response [a in b where assertIn(a,b)]
        self.assertEqual(response.status_code, 200, msg='Should check that mythology has a successful response.')
        self.assertIsNotNone(json_response, msg="Should check that an API response was successfully received and parsed into a JSON format.")        
        self.assertIsInstance(json_response, dict, msg='Should check that json_response is a dictionary.')
        self.assertIn("trivia_categories", json_response, msg='Should check that the trivia_categories key is present in the dictionary json_response.')

    # test specific json category with unittest
    def test_get_specific_json_category_with_unittest(self):
        # use unittest to simulate an external API request    
        mythology_url = f"https://opentdb.com/api.php?amount=50&category=20"
        response = requests.get(mythology_url)

        # test if there's a successful get request for a specific category
        if response.status_code == 200:
            json_response = response.json()

        # test if there's an unsuccessful get request for a specific category
        else:
            error_message = f"Unable to retrieve the specific category - Status code:{response.status_code}"
            print(error_message)
            json_response = None

        # assert that get request renders succesfully
        # 
        self.assertEqual(response.status_code, 200, msg='Should check that mythology has a successful response.')
        self.assertIsNotNone(json_response, msg="Should check that the mythology API response was successfully received and parsed into a JSON format.")        
        self.assertIsInstance(json_response, dict, msg='Should check that the json_response is a dictionary.')
        self.assertIn("results", json_response, msg='Should check that the results key is present in the dictionary json_response.')
'''