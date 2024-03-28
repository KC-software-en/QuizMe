### Run commands for testing and coverage ###
# coverage erase
# python manage.py test Entertainment.tests.test_views
# coverage run --source='.' manage.py test Entertainment
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

# import functions from utils.py called in views
from ..utils import (
    get_json_categories,
    find_model,
    get_specific_json_category,
    mix_choices,
)
# Import all modules from the 'models' package
from ..models import *

# import the views to be tested
from Entertainment.views import *
from user_auth.views import *


### Create a testcases for the views. ###
### Test for Index_en view ###
class Test_index_en_View(TestCase):
    def setUp(self):
        # Create a RequestFactory instance.
        self.factory = RequestFactory()

    # patch the functions in the Entertainment views.
    @patch('Entertainment.views.get_json_categories')
    @patch('Entertainment.views.get_category_names')
    @patch('Entertainment.views.category_objects')
    def test_index_en_edu(self, mock_category_objects, mock_get_category_names, mock_get_json_categories):
        # Assign the mocks with their return values.
        mock_get_json_categories.return_value = 'mocked_categories'
        mock_get_category_names.return_value = ['mocked_category_name']
        mock_category_objects.return_value = 'mocked_question_selection'

        # This line makes a request to the '/Entertainment/' endpoint.
        request = self.factory.get('/Entertainment/')
        # Storing quiz results and selected question IDs in the session.
        request.session = {'quiz_result': 'some_result', 'question_selection_ids': [1, 2, 3]}

        response = index_en(request)
        
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
        request = Mock()
        # Mocking the user object for testing purposes.
        request.user = Mock()


        # Mock the necessary functions.
        mock_get_json_categories = Mock(return_value={'categories': [{'name': 'category1'}, {'name': 'category2'}]})
        mock_get_category_names = Mock(return_value=['category1', 'category2'])
        mock_find_model = Mock(return_value=Mock())
        mock_get_object_or_404 = Mock(return_value=Mock(
            pk=1,
            correct_answer='Answer',
            choices='["Choice 1", "Choice 2", "Choice 3"]'
        ))

        # Patch the necessary functions in views.
        with patch('Entertainment.views.get_json_categories',mock_get_json_categories), \
             patch('Entertainment.views.get_category_names', mock_get_category_names), \
             patch('Entertainment.views.find_model', mock_find_model), \
             patch('Entertainment.views.get_object_or_404', mock_get_object_or_404):
            response = detail(request, 'category1', 1)
        
        # Assert that the correct template is rendered.
        self.assertEqual(response, 'entertainment/en_detail.html')

        # Assert that the context contains the expected values
        self.assertEqual(response.context_data['question'].pk, 1)
        self.assertEqual(response.context_data['question'].correct_answer, 'Answer')
        self.assertEqual(response.context_data['choices'], ['Choice 1', 'Choice 2', 'Choice 3'])
        self.assertEqual(response.context_data['category_name'], 'category1')

    def test_detail_view_with_invalid_question(self):
        # Create a mock request with category_name and question_id.
        request = Mock()
        request.user = Mock()

        # Mock the necessary functions.
        mock_get_json_categories = Mock(return_value={'trivia_categories"': [{'name': 'category1'}, {'name': 'category2'}]})
        mock_get_category_names = Mock(return_value=['category1', 'category2'])
        mock_find_model = Mock(return_value=Mock())
        mock_get_object_or_404 = Mock(side_effect=Http404)

        # Patch the necessary functions in views.
        with patch('Entertainment.views.get_json_categories', mock_get_json_categories), \
             patch('Entertainment.views.get_category_names', mock_get_category_names), \
             patch('Entertainment.views.find_model', mock_find_model):
                response = detail(request, 'category1', 2)             

        # Assert that the correct template is rendered.
        self.assertTemplateUsed(response, 'entertainment/en_detail.html')

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
        # Fetch the 'Music' results using the client's GET request.
        req = self.client.get(reverse('Entertainment:results', args=['Music']))
        # Initialize session middleware with the provided request handler.
        middleware = SessionMiddleware(get_response=req)
        # This method is called before URL resolution and view routing.
        middleware.process_request(request)
        # Save the session data.
        request.session.save()

        category_name = 'Music'

        # Call the view function.
        response = results(request, category_name)

        # Assertions.
        self.assertEqual(response.status_code, 200)

    def test_results_view_with_an_authenticated_user(self):
        # Log in the test user.
        self.client.login(username='testuser', password='testpassword')

        # Replace 'your_category_name' with the actual category name.
        category_name = 'Music'

        # Call the view function.
        response = self.client.get(reverse('Entertainment:results', args=[category_name]))

        # Assertions.
        # Check if the response status code is 200 (OK).
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used.
        self.assertTemplateUsed(response, 'edu_quiz/index.html')
        # Check if the 'result' and 'category_name' are in the context.
        self.assertIn('result', response.context)
        self.assertEqual(response.context['category_name'], category_name)
        
### Test for the selection views. ###
class SelectionTestCase(TestCase): 
    def setup(self):
        # Create a RequestFactory instance.
        self.factory = RequestFactory()      
    @patch('Entertainment.views.ast') 
    def test_selection_with_a_valid_category_and_question(self, mock_ast):
        # Mock functions.
        get_json_categories = MagicMock(return_value={"Film": {}, "Music": {}})
        get_category_names = MagicMock(return_value=["Film", "Music"])
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
        response = selection(request, 'Music', 1)

        # Assertions.
        # Assert that the correct template is rendered
        self.assertEqual(response, 'entertainment/en_detail.html')
        self.assertTemplateUsed,(response, 'entertainment/en_detail.html')
        # Assert that ast.literal_eval was called once with the return value of get_object_or_404.choices
        ast.literal_eval.assert_called_once_with(get_object_or_404.return_value.choices)
        # Assert that the `model.objects.get` method was called exactly once with the primary key (`pk`) from the `request.POST['choice']`.
        model.objects.get.assert_called_once_with(pk=request.POST['choice'])
        # Check if the function get_json_categories() returns the expected value.
        assert get_json_categories() == {"Film": {}, "Music": {}}, "get_json_categories did not return the expected value"
        # Check if the function get_category_names() returns the expected value
        assert get_category_names() == ["Film", "Music"], "get_category_names did not return the expected value"
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
        with patch('Entertainment.views.get_json_categories', get_json_categories), \
             patch('Entertainment.views.get_category_names', get_category_names), \
             patch('Entertainment.views.find_model', find_model), \
             patch('Entertainment.views.get_object_or_404', get_object_or_404):
            response = selection(request, 'category1', 2)

        # Assertions.
        # Assert that get_object_or_404 was called.
        get_object_or_404.assert_called_once()    
        get_object_or_404.assert_called_with('category1', 1)
        
        # Assert that the correct template is rendered.
        self.assertEqual(response, 'entertainment/en_detail.html')
        self.assertTemplateUsed,(response, 'entertainment/en_detail.html')

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
        self.assertEqual(response.url, reverse('Entertainment:index_en'))  # Assert redirect URL is the correct url.

    # Test for the try new quiz view  with results.
    # Patch reverse function.
    @patch('django.shortcuts.reverse')  
    def test_try_new_quiz_with_a_valid_result(self, mock_reverse):
        # Mock reverse function.
        mock_reverse.return_value = '/Entertainment/try_new_quiz/'  

        # Create a mock request object with "quiz_result" in the session.
        request = MagicMock()
        request.session = {'quiz_result': 5}

        # Call the function.
        response = try_new_quiz(request)

        # Assert expected behaviors.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/Entertainment/')

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
        self.assertEqual(response.url, reverse('Entertainment:index_en'))  # Assert redirect URL is the correct url.
