# import the required libraries
# import ast safely evaluate strings containing Python literal structures e.g.strings, lists, dicts
# use to convert str into list
import ast 
from django.template.response import SimpleTemplateResponse
from django.template.response import TemplateResponse
from django.http import Http404, HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from unittest.mock import patch, MagicMock, Mock
from django.test.client import RequestFactory, Client
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User

# import functions from utils.py called in views
from ..utils import (
    get_json_categories,
    get_category_names,
    get_specific_json_category,
    mix_choices,
)

from ..models import *

# import the views to be tested
from ..views import index, detail, index_edu, selection, try_new_quiz, results

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

# Test for the Detail view  
class TestDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('Education.views.get_json_categories')
    @patch('Education.views.get_category_names')
    @patch('Education.views.get_object_or_404')
    @patch('Education.views.ast')
    def test_detail_view(self, mock_ast, mock_get_object_or_404, mock_get_category_names, mock_get_json_categories):
        # Mocking necessary functions and objects
        mock_request = self.factory.get(detail, kwargs={'category_name': 'History', 'question_id': 1})
        mock_response = MagicMock()
        mock_get_json_categories.return_value = mock_response
        mock_category_names = ['History']
        mock_get_category_names.return_value = mock_category_names
        mock_question = MagicMock()
        mock_get_object_or_404.return_value = mock_question
        mock_convert_choices = ['choice1', 'choice2']
        mock_ast.literal_eval.return_value = mock_convert_choices

        # Call the view function
        response = detail(mock_request, 'History', 1)

        # Assertions
        mock_get_json_categories.assert_called_once()
        mock_get_category_names.assert_called_once_with(mock_response)
        mock_get_object_or_404.assert_called_once()
        mock_ast.literal_eval.assert_called_once_with(mock_question.choices)
        self.assertEqual(response.status_code, 200)
        self.assertIn('question', response.context)
        self.assertIn('choices', response.context)
        self.assertIn('category_name', response.context) 

# Test for the try new quiz view  
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
  self.assertEqual(response['Location'], '/Education/try_new_quiz/')

  # Assert "quiz_result" is deleted
  self.assertNotIn('quiz_result', request.session)

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

    def test_try_new_quiz_without_quiz_result_in_session(self):
        # Create a session without 'quiz_result'
        request = self.factory.get(try_new_quiz)

        # Call the view function
        response = try_new_quiz(request)

        # Assertions
        self.assertNotIn('quiz_result', request.session)  # Assert session data has not been modified
        self.assertIsInstance(response, HttpResponseRedirect)  # Assert response is a redirect
        self.assertEqual(response.url, reverse('Education:index_edu'))  # Assert redirect URL is correct  

# Test for the results view
    @patch('django.shortcuts.render')  # Patch render function
    def test_results(self, mock_render):
        # Mock request object
        request = MagicMock()

        # Scenario 1: "quiz_result" present in session
        request.session['quiz_result'] = {'score': 10, 'max_score': 10}
        category_name = 'Math'

        # Call function and assert rendering
        mock_render.return_value.status_code = 200  # Set mock response status code
        response = results(request, category_name)
        self.assertEqual(response.status_code, 200)

        # Assert context dictionary
        context = mock_render.call_args[1]['context']
        self.assertEqual(context['result'], request.session['quiz_result'])
        self.assertEqual(context['category_name'], category_name)

        # Scenario 2: "quiz_result" not present in session
        del request.session['quiz_result']

        # Call function and assert rendering (should not redirect)
        mock_render.return_value.status_code = 200
        response = results(request, category_name)
        self.assertEqual(response.status_code, 200)

        # Assert context dictionary has empty result
        context = mock_render.call_args[1]['context']
        self.assertEqual(context['result'], None)
        self.assertEqual(context['category_name'], category_name)

        # Scenario 3: Invalid category name
        invalid_category_name = 'Invalid'

        # Mock render to raise exception (e.g., Http404)
        mock_render.side_effect = Exception('Template not found')

        # Call function and expect exception
        with self.assertRaises(Exception):
            results(request, invalid_category_name)       

    def test_results_view_with_quiz_result_in_session(self):
        # Create a session with 'quiz_result'
        session = {'quiz_result': 'some_result'}
        request = self.factory.get('<str:category_name>results/')
        request.session = session

        # Call the view function
        response = results(request, 'some_category')

        # Assertions
        self.assertEqual(response.status_code, 200)  # Assert response status code is OK
        self.assertEqual(response.template_name, 'edu_quiz/edu_result.html')  # Assert correct template used
        self.assertEqual(response.context_data['result'], 'some_result')  # Assert 'result' context data is correct
        self.assertEqual(response.context_data['category_name'], 'some_category')  # Assert 'category_name' context data is correct

    def test_results_view_without_quiz_result_in_session(self):
        # Create a session without 'quiz_result'
        request = self.factory.get('<str:category_name>results/')

        # Call the view function
        response = results(request, 'some_category')

        # Assertions
        self.assertEqual(response.status_code, 200)  # Assert response status code is OK
        self.assertIsInstance(response, TemplateResponse)  # Assert response is a TemplateResponse
        self.assertEqual(response.template_name, 'edu_quiz/edu_result.html')  # Assert correct template used
        self.assertIsNone(response.context_data['result'])  # Assert 'result' context data is None
        self.assertEqual(response.context_data['category_name'], 'some_category')  # Assert 'category_name' context data is correct    

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

        # Assertions
        self.assertIn('category_names', response.context_data)
        self.assertIn('question_selection', response.context_data)
        self.assertIn('first_question_id', response.context_data)

# Test for the selection views
class SelectionTestCase(TestCase):       
    @patch('Education.views.ast') 
    def test_selection_valid_category_and_question(self, mock_ast):
        # Mock functions
        get_json_categories = MagicMock(return_value={"Mythology": {}, "History": {}})
        get_category_names = MagicMock(return_value=["Mythology", "History"])
        get_object_or_404 = MagicMock()
        model = MagicMock()
        model.objects.get = MagicMock()

        # Set request object with valid choice
        request = MagicMock()
        request.POST = {'choice': 1}
        mock_convert_choices = ['choice1', 'choice2']
        mock_ast.literal_eval.return_value = mock_convert_choices
        mock_question = MagicMock()

        # Call function
        selection(request, "History", 1)
        
        # Assertions
        ast.literal_eval.assert_called_once_with(get_object_or_404.return_value.choices)
        model.objects.get.assert_called_once_with(pk=request.POST['choice'])
        assert get_json_categories() == {"Mythology": {}, "History": {}}, "get_json_categories did not return the expected value"
        assert get_category_names() == ["Mythology", "History"], "get_category_names did not return the expected value"
        mock_ast.literal_eval.assert_called_once_with(mock_question.choices)
