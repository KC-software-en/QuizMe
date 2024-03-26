### Run commands for testing and coverage ###
# coverage erase
# python manage.py test Education.tests.test_views
# coverage run --source='.' manage.py test Education
# coverage report
# coverage html

### Documentation used for unnit testing and Mocks.###
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
# https://vegibit.com/how-to-test-django-views/
# https://stackoverflow.com/questions/11885211/how-to-write-a-unit-test-for-a-django-view
# https://docs.python.org/3/library/unittest.mock.html

### import the required libraries ###
# import ast safely evaluate strings containing Python literal structures e.g.strings, lists, dicts
import ast 
# Importing the HttpResponseRedirect class from django.http.
# This class returns an HTTP 302 status code, indicating that the URL resource was found
from django.http import HttpResponseRedirect
# Importing the Http404 exception from django.http.
# This exception is used to return a standard error page with an HTTP 404 status code.
from django.http import Http404
# Importing the TestCase class from django.test module which is used to create testcases.
from django.test import TestCase
# Importing the reverse function from django.urls allows us to generate URLs dynamically based on view names defined in your project's URL.
from django.urls import reverse
# Import the User model and AnonymousUser from Django's authentication system to create dumby users. 
from django.contrib.auth.models import User, AnonymousUser
# Importing necessary modules for mocking: patch, MagicMock, and Mock
from unittest.mock import patch, MagicMock, Mock
# RequestFactory returns a request, while Client returns a response.
from django.test.client import RequestFactory, Client
# Importing HttpResponse and HttpRequest from django.http.
from django.http import HttpResponse, HttpRequest
# Importing the SessionMiddleware for handling sessions in Django.
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# import apps to dynamically fetch a model in detail() & selection() view
from django.apps import apps

# import functions from utils.py called in views
from ..utils import (
    get_json_categories,
    get_category_names,
    get_specific_json_category,
    mix_choices,
)
# Import all modules from the 'models' package
from ..models import *

# import the views to be tested
from ..views import *
from user_auth.views import *


### Create a testcases for the views. ###
# Test for the index view.
class TestIndexView(TestCase):
    # Create a setUp method to create a user which is logged in before each test.
    def setUp(self):
        # Create a RequestFactory instance.
        self.factory = RequestFactory()

    def test_session_key_exists_in_index_view(self):
        # Create a request with 'quiz_result' in session in the index page.
        request = self.factory.get('/')
        request.session = {'quiz_result': 'some_value'}

        # Call the index view function/method.
        response = index(request)

        # Check if 'quiz_result' is removed from the index session.
        self.assertNotIn('quiz_result', request.session)
        self.assertIsInstance(response, HttpResponse)

    def test_session_key_not_exists_in_index_view(self):
        # Create a request without 'quiz_result' in index session.
        request = self.factory.get('/')
        request.session = {}

        # Call the index view function/method.
        response = index(request)

        # Check if 'quiz_result' is not removed from the index session.
        self.assertNotIn('quiz_result', request.session)
        self.assertIsInstance(response, HttpResponse)

### Test for Index_edu view ###
class TestIndexEduView(TestCase):
    def setUp(self):
        # Create a RequestFactory instance.
        self.factory = RequestFactory()

    # patch the functions in the Education views.
    @patch('Education.views.get_json_categories')
    @patch('Education.views.get_category_names')
    @patch('Education.views.category_objects')
    def test_index_edu(self, mock_category_objects, mock_get_category_names, mock_get_json_categories):
        # Assign the mocks with their return values.
        mock_get_json_categories.return_value = 'mocked_categories'
        mock_get_category_names.return_value = ['mocked_category_name']
        mock_category_objects.return_value = 'mocked_question_selection'

        # This line makes a request to the '/Education/' endpoint.
        request = self.factory.get('/Education/')
        # Storing quiz results and selected question IDs in the session.
        request.session = {'quiz_result': 'some_result', 'question_selection_ids': [1, 2, 3]}

        response = index_edu(request)
        
        # Assertions.
        self.assertEqual(response.status_code, 200)
        mock_get_json_categories.assert_called_once()
        mock_get_category_names.assert_called_once_with('mocked_categories')
        mock_category_objects.assert_called_once_with(request, 'mocked_category_name')

### Test for the Detail view ###
class TestDetailView(TestCase):    
    def setUp(self):
        # Create a client instance.
        self.client = Client()

    def test_detail_view_with_valid_question(self):
        # Create a mock request with category_name and question_id.
        request = self.client.get('/Education/category/1')
        # Mocking the user object for testing purposes.
        request.user = Mock()


        # Mock the necessary functions.
        get_json_categories = Mock(return_value={'categories': [{'name': 'category1'}, {'name': 'category2'}]})
        get_category_names = Mock(return_value=['category1', 'category2'])
        find_model = Mock(return_value=Mock())
        get_object_or_404 = Mock(return_value=Mock(
            pk=1,
            correct_answer='Answer',
            choices='["Choice 1", "Choice 2", "Choice 3"]'
        ))

        # Patch the necessary functions in views.
        with patch('Education.views.get_json_categories', get_json_categories), \
             patch('Education.views.get_category_names', get_category_names), \
             patch('Education.views.find_model', find_model), \
             patch('Education.views.get_object_or_404', get_object_or_404):
            response = detail(request, 'category1', 1)
        
        # Assert that the correct template is rendered.
        self.assertEqual(response, 'edu_quiz/edu_detail.html')

        # Assert that the context contains the expected values
        self.assertEqual(response.context_data['question'].pk, 1)
        self.assertEqual(response.context_data['question'].correct_answer, 'Answer')
        self.assertEqual(response.context_data['choices'], ['Choice 1', 'Choice 2', 'Choice 3'])
        self.assertEqual(response.context_data['category_name'], 'category1')

    def test_detail_view_with_invalid_question(self):
        # Create a mock request with category_name and question_id.
        request = self.client.get('<str:category_name>/<int:question_id>/detail/')
        request.user = Mock()

        # Mock the necessary functions.
        get_json_categories = Mock(return_value={'trivia_categories"': [{'name': 'category1'}, {'name': 'category2'}]})
        get_category_names = Mock(return_value=['category1', 'category2'])
        find_model = Mock(return_value=Mock())
        get_object_or_404 = Mock(side_effect=Http404)

        # Patch the necessary functions in views.
        with patch('Education.views.get_json_categories', get_json_categories), \
             patch('Education.views.get_category_names', get_category_names), \
             patch('Education.views.find_model', find_model):
                response = detail(request, 'category1', 2)             

        # Assert that the correct template is rendered.
        self.assertEqual(response.template_name, 'edu_quiz/edu_detail.html')

        # Assert that the context contains the expected values.
        self.assertIsNone(response.context_data['question'])
        self.assertEqual(response.context_data['choices'], [])
        self.assertEqual(response.context_data['category_name'], 'category1')

    

### Test for the results view. ###
class ResultsViewTest(TestCase):
    def setUp(self):
        # Create a test user instance.
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_results_view_that_requires_login(self):
        # Create a request object.
        request = HttpRequest()
        request.user = self.user
        # Fetch the 'History' results using the client's GET request.
        req = self.client.get(reverse('Education:results', args=['History']))
        # Initialize session middleware with the provided request handler.
        middleware = SessionMiddleware(get_response=req)
        # This method is called before URL resolution and view routing.
        middleware.process_request(request)
        # Save the session data.
        request.session.save()

        category_name = 'History'

        # Call the view function.
        response = results(request, category_name)

        # Assertions.
        self.assertEqual(response.status_code, 200)

    def test_results_view_with_an_authenticated_user(self):
        # Log in the test user.
        self.client.login(username='testuser', password='testpassword')

        # Replace 'your_category_name' with the actual category name.
        category_name = 'History'

        # Call the view function.
        response = self.client.get(reverse('Education:results', args=[category_name]))

        # Assertions.
        # Check if the response status code is 200 (OK).
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used.
        self.assertTemplateUsed(response, 'edu_quiz/edu_result.html')
        # Check if the 'result' and 'category_name' are in the context.
        self.assertIn('result', response.context)
        self.assertEqual(response.context['category_name'], category_name)
        
### Test for the selection views. ###
class SelectionTestCase(TestCase): 
    def setup(self):
        # Create a RequestFactory instance.
        self.factory = RequestFactory()      
    @patch('Education.views.ast') 
    def test_selection_with_a_valid_category_and_question(self, mock_ast):
        # Mock functions.
        get_json_categories = MagicMock(return_value={"Mythology": {}, "History": {}})
        get_category_names = MagicMock(return_value=["Mythology", "History"])
        get_object_or_404 = MagicMock()
        model = MagicMock()
        model.objects.get = MagicMock()

        # Set request object with valid choice.
        request = MagicMock()
        request.POST = {'choice': 1}
        mock_convert_choices = ['choice1', 'choice2']
        mock_ast.literal_eval.return_value = mock_convert_choices
        mock_question = MagicMock()

        # Call function.
        response = selection(request, 'History', 1)

        # Assertions.
        # Assert that the correct template is rendered
        self.assertEqual(response, 'edu_quiz/edu_detail.html')
        self.assertTemplateUsed,(response, 'edu_quiz/edu_detail.html')
        # Assert that ast.literal_eval was called once with the return value of get_object_or_404.choices
        ast.literal_eval.assert_called_once_with(get_object_or_404.return_value.choices)
        # Assert that the `model.objects.get` method was called exactly once with the primary key (`pk`) from the `request.POST['choice']`.
        model.objects.get.assert_called_once_with(pk=request.POST['choice'])
        # Check if the function get_json_categories() returns the expected value.
        assert get_json_categories() == {"Mythology": {}, "History": {}}, "get_json_categories did not return the expected value"
        # Check if the function get_category_names() returns the expected value
        assert get_category_names() == ["Mythology", "History"], "get_category_names did not return the expected value"
        # Assert that the 'mock_ast.literal_eval' function was called exactly once with the 'mock_question.choices' argument.
        mock_ast.literal_eval.assert_called_once_with(mock_question.choices)

    def test_selection_view_with_no_model(self):
        # Create a client instance.
        self.client = Client()
        # Create a Mock request.
        request = MagicMock()        
        request.user = Mock()

        # Mock the necessary functions.        
        find_model = Mock(return_value=Mock())
        get_object_or_404 = Mock(return_value=Mock(
            pk=1,
            correct_answer='Choice 1',
            choices='["Choice 1", "Choice 2", "Choice 3"]'
        ))

        # Patch the necessary functions in views.
        with patch('Education.views.get_json_categories', get_json_categories), \
             patch('Education.views.get_category_names', get_category_names), \
             patch('Education.views.find_model', find_model), \
             patch('Education.views.get_object_or_404', get_object_or_404):
            response = selection(request, 'category1', 2)

        # Assertions.
        # Assert that get_object_or_404 was called.
        get_object_or_404.assert_called_once()    
        get_object_or_404.assert_called_with('category1', 1)
        
        # Assert that the correct template is rendered.
        self.assertEqual(response, 'edu_quiz/edu_detail.html')
        self.assertTemplateUsed,(response, 'edu_quiz/edu_detail.html')

        # Assert that the error message is present in the response.
        self.assertIn("You didn't select a choice.", response['error_message'])


        # Assert that the context contains the expected values.
        self.assertEqual(response.context_data['question'].pk, 1)
        self.assertEqual(response.context_data['question'].correct_answer, 'Choice 1')
        self.assertEqual(response.context_data['choices'], ['Choice 1', 'Choice 2', 'Choice 3'])
        self.assertEqual(response.context_data['category_name'], 'category1')      
      
### Test for the try new quiz view. ###
class TestTryNewQuiz(TestCase):
    def setUp(self):
        # Create a RequestFactory instance.
        self.factory = RequestFactory()

    def test_try_new_quiz_with_quiz_result_in_session(self):
        # Create a session with 'quiz_result'.
        session = {'quiz_result': 5}
        request = self.factory.get(try_new_quiz)
        request.session = session

        # Call the view function.
        response = try_new_quiz(request)

        # Assertions.
        self.assertNotIn('quiz_result', request.session)  # Assert session data has not been deleted
        self.assertIsInstance(response, HttpResponseRedirect)  # Assert response is a redirect reponse.
        self.assertEqual(response.url, reverse('Education:index_edu'))  # Assert redirect URL is the correct url.

    # Test for the try new quiz view  with results.
    # Patch reverse function.
    @patch('django.shortcuts.reverse')  
    def test_try_new_quiz_with_a_valid_result(self, mock_reverse):
        # Mock reverse function.
        mock_reverse.return_value = '/Education/try_new_quiz/'  

        # Create a mock request object with "quiz_result" in the session.
        request = MagicMock()
        request.session = {'quiz_result': 5}

        # Call the function.
        response = try_new_quiz(request)

        # Assert expected behaviors.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/Education/')

        # Assert "quiz_result" is deleted from the sessions.
        self.assertNotIn('quiz_result', request.session) 

    def test_try_new_quiz_without_quiz_result_in_session(self):
        # Create a session without 'quiz_result' in the session.
        request = RequestFactory().get(try_new_quiz)
        # Add middleware manualy.
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()

        # Call the view function.
        response = try_new_quiz(request)
        
         # Assertions.
        self.assertNotIn('quiz_result', request.session)  # Assert session data has not been changed.
        self.assertIsInstance(response, HttpResponseRedirect)  # Assert response is a HttpResponseRedirect.
        self.assertEqual(response.url, reverse('Education:index_edu'))  # Assert redirect URL is the correct url.
       
'''
A class that tests finding a model.
'''
# create a class that tests finding a model.         
@patch('Education.views.apps.get_model')
class TestFindModel(TestCase):
    # setup
    def setUp(self):
        # create a RequestFactory instance for generating mock HTTP requests during testing
        self.factory = RequestFactory()

        # Create a user object
        self.user = User.objects.create(username='test_user')            
            
    # create a test that locates a model in the app    
    def test_find_model_success(self, mock_get_model): ##, mock_get_object_or_404
        # mock the category_name that will be used to find a model
        mock_category_name_ok = 'Mythology'               

        # create a MagicMock object to mock the behaviour of the Mythology class
        # use spec=Mythology to ensure that mock_model behaves like an instance of the Mythology class
        # https://docs.python.org/3.7/library/unittest.mock.html#the-mock-class
        # set the return value of mock_get_model to be the mock_model object
        mock_model = MagicMock(spec=Mythology)     
        mock_get_model.return_value = mock_model
        
        # call the get_model function with its args app name & model name
        result = apps.get_model('Education', mock_category_name_ok)
        
        # assert that the result object is an instance of the same class as mock_model
        # https://docs.python.org/3.7/library/unittest.html?highlight=assertisinstance#unittest.TestCase.assertIsInstance
        # assert that the result is not none, indicating successful retrieval
        self.assertIsInstance(result, type(mock_model), msg='Should check that the response to the function get_model is a model instance.')
        self.assertIsNotNone(result, msg='Should check that the model is not none.')        
                
    # test for an error raised if globals does not have a model for a category name    
    def test_find_model_fail(self, mock_get_model):            
        # mock the arguments for the detail() function
        mock_category_name_absent = 'Sports'   
        mock_question_id = 20     

        # mock the get_model function to raise a LookupError for an incorrect category_name (i.e. no corresponding model)                       
        mock_get_model.side_effect = LookupError
                
        # Create a GET request for the view
        # set the user attribute for the request - required for the login decorator
        request = self.factory.get(reverse('Education:edu_detail', args=['Sports', 20]))
        request.user = self.user

        # Call the view function with the GET request & its actual arguments        
        response = detail(request, mock_category_name_absent, mock_question_id)        

        # simulate the behaviour where the model is not found in the global namespace
        # raise an error when calling find_model() with an invalid category name
        # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#exceptions
        # according to documentation, an exception not visible to the test client is Http404 
        # - :. check response.status_code in test because assertRaises(Http404) gives AssertionError: Http404 not raised
        self.assertEqual(response.status_code, 200, msg='Should check that the status_code is 200 for the error message shown on detail template.')
        # assert that the error message was returned in the response content
        # - use b syntax to create a byte string literal. the content of a HTTP response is binary data - content get returned as a byte string
        self.assertIn(b"Unable to find the model", response.content, msg='Should check that None was returned for a model not located.')

        
        

