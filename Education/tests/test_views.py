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

#  import unittest to write tests that are not necessarily tied to Django and can be used in any Python project e.g. get API response from open trivia db
import unittest

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

# https://www.django-rest-framework.org/api-guide/testing/#api-test-cases ######## refer back ###
class TestJsonResponse(unittest.TestCase):
    def setUp(self):
        pass

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

    # test json categories by calling its function from views 
    def test_get_json_categories_call(self):      
        response = views.get_json_categories()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertIn('trivia_categories', response)

    # test json specific categories by calling its function from views  
    def test_get_specific_json_category_call(self):
        response = views.get_specific_json_category(quantity=5, category=20)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertIn('results', response)        

'''
Create ...
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
        response = get_questions_and_choices(request, quantity=50, category=20)

        # Assert that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # add more assertions 

    def test_get_questions_and_choices_no_questions(self):
        # Create a GET request for the view
        request = self.factory.get('/path/to/your/view/50/20/')
        
        # Mock the get_specific_json_category function to return a response without questions
        with patch('your_app.views.get_specific_json_category') as mock_get_specific_json:
            mock_get_specific_json.return_value = {'results': []}

            # Call the view function with the GET request
            response = get_questions_and_choices(request, quantity=50, category=20)

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

