# import the required libraries
# import ast safely evaluate strings containing Python literal structures e.g.strings, lists, dicts
# use to convert str into list
### Run commands for test ###
# coverage erase
# python manage.py test Education.tests.test_views
# coverage run --source='.' manage.py test Education
# coverage report
# coverage html

import ast 
from django.template.response import SimpleTemplateResponse
from django.template.response import TemplateResponse
from django.http import Http404, HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.hashers import make_password
from unittest.mock import patch, MagicMock, Mock
from django.test.client import RequestFactory, Client
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# import functions from utils.py called in views
from ..utils import (
    get_json_categories,
    get_category_names,
    get_specific_json_category,
    mix_choices,
)

from ..models import *

# import the views to be tested
from Education.views import *
from user_auth.views import *

# create a test case for the views
# tests for index view
class TestViews(TestCase):

    # create a setUp method to create a user and login before each test
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password=make_password('password'))
        self.client.login(username='testuser', password='password')

    def test_index_view(self):
    # test that index view returns correct response
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')    
  
# Test for the index edu view
class IndexEduTestCase(TestCase):
    def setUp(self):
        # Create a mock request
        self.factory = RequestFactory()
        self.request = self.factory.get('/Education/')
        self.request.session = {'question_selection_ids': [1, 2, 3]}  # Example session data

    @patch('Education.views.get_json_categories')
    @patch('Education.views.get_category_names')
    @patch('Education.views.category_objects')
    def test_index_edu(self, mock_category_objects, mock_get_category_names, mock_get_json_categories):
        # Mock the necessary functions
        mock_get_json_categories.return_value = {'categories': [{'name': 'Math'}, {'name': 'Science'}]}
        mock_get_category_names.return_value = ['Math', 'Science']
        mock_category_objects.return_value = [{'id': 1, 'text': 'Question 1'}, {'id': 2, 'text': 'Question 2'}]

        # Call the view function
        response = index_edu(self.request)
        expected_categories = {'categories': [{'name': 'Math'}, {'name': 'Science'}]}
        expected_names = ['Math', 'Science']
        expected_objects = [
        {'id': 1, 'text': 'Question 1'},
        {'id': 2, 'text': 'Question 2'}
        ]
        category_objects = mock_category_objects()

        # Assertions        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_get_json_categories(), expected_categories)
        self.assertEqual(mock_get_category_names(), expected_names)
        self.assertEqual(len(category_objects), len(expected_objects))
        for i in range(len(expected_objects)):
            self.assertEqual(category_objects[i], expected_objects[i])

# Test for the Detail view  
class TestDetailView(TestCase):
    # Still need to test for.
    pass
    
# Test for the results view
class ResultsViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_results_view_requires_login(self):
        # Create a request object
        request = HttpRequest()
        request.user = self.user
        req = self.client.get(reverse('Education:results', args=['History']))
        middleware = SessionMiddleware(get_response=req)
        middleware.process_request(request)
        request.session.save()

        category_name = 'History'

        # Call the view function
        response = results(request, category_name)

        self.assertEqual(response.status_code, 200)

    def test_results_view_with_authenticated_user(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Replace 'your_category_name' with the actual category name
        category_name = 'History'

        # Call the view function
        response = self.client.get(reverse('Education:results', args=[category_name]))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # You can add more assertions here based on your view's behavior

        # Example: Check if the correct template is used
        self.assertTemplateUsed(response, 'edu_quiz/edu_result.html')

        # Example: Check if the 'result' and 'category_name' are in the context
        self.assertIn('result', response.context)
        self.assertEqual(response.context['category_name'], category_name)

# Test for the selection views
class SelectionTestCase(TestCase):
    # Still need to test for.
    pass

# Test for the try new quiz view  
class TestTryNewQuiz(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_try_new_quiz_with_quiz_result_in_session(self):
        # Create a session with 'quiz_result'
        session = {'quiz_result': 5}
        request = self.factory.get(try_new_quiz)
        request.session = session

        # Call the view function
        response = try_new_quiz(request)

        # Assertions
        self.assertNotIn('quiz_result', request.session)  # Assert session data has been deleted
        self.assertIsInstance(response, HttpResponseRedirect)  # Assert response is a redirect
        self.assertEqual(response.url, reverse('Education:index_edu'))  # Assert redirect URL is correct

# Test for the try new quiz view  with results
    @patch('django.shortcuts.reverse')  # Patch reverse function
    def test_try_new_quiz_with_result(self, mock_reverse):
        # Mock reverse function
        mock_reverse.return_value = '/Education/try_new_quiz/'  # Replace with the expected redirect URL

        # Create a mock request object with "quiz_result" in the session
        request = MagicMock()
        request.session = {'quiz_result': 5}

        # Call the function
        response = try_new_quiz(request)

        # Assert expected behavior
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/Education/')

        # Assert "quiz_result" is deleted
        self.assertNotIn('quiz_result', request.session) 

    def test_try_new_quiz_without_quiz_result_in_session(self):
        # Create a session without 'quiz_result'
        request = RequestFactory().get(try_new_quiz)
        # Add middleware manualy
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()

        # Call the view function
        response = try_new_quiz(request)

        # Assertions
        self.assertNotIn('quiz_result', request.session)  # Assert session data has not been modified
        self.assertIsInstance(response, HttpResponseRedirect)  # Assert response is a redirect
        self.assertEqual(response.url, reverse('Education:index_edu'))  # Assert redirect URL is correct 
