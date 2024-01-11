# Regular expressions are powerful tools for pattern matching and manipulation of strings
# U flag is used to indicate that the regular expression pattern should be treated as a Unicode string. 
# Unicode is a standard for representing characters from most of the world's languages, 
from re import U # delete if not used later

# import from urllib to work with URL requests & the response handling process when making HTTP requests
from urllib import request, response

# https://docs.djangoproject.com/en/5.0/intro/tutorial05/#id7
# reverse function is used in Django to generate URLs for views based on their names or patterns
from django.urls import reverse

# import all views
# (had to use this structure so that response object would recognise views)
from .. import views

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
# import RequestFactory to generate a HttpRequest objects & simulate HTTP requests (faster than using Client)
# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#the-test-client
# https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#the-request-factory
# import base class for all Django test cases (for writing tests, including test assertions, database setup and teardown, and other testing infrastructure)
from django.test import TestCase, TransactionTestCase, RequestFactory, Client

# import AnonymousUser model - a special type of user object representing an unauthenticated user or a user who is not logged in
from django.contrib.auth.models import AnonymousUser

# import the Question model
from ..models import Question

# import timezone for Question instance
from django.utils import timezone

# the view renders an HTTP 404 error if a question with the requested ID doesn’t exist.
from django.shortcuts import get_object_or_404
from django.http import Http404

# import logging then comment out after debugging view response to pass assertions
# import logging

#############################################################################################
#############################################################################################
# Create your tests here. Use `py manage.py test to run tests in cmd
# after writing a test, run in cmd & it will say fail. 
# next, go to views.py and create the views. Then it should pass
# run coverage after tests

'''
Create a class to test the views of the Education quiz application.
'''
# test the views with RequestFactory
class TestEducationViews(TransactionTestCase):
    '''
    Setup the required data to test the views of Education.
    '''
    # setup RequestFactory for all views
    # setup a user who is not logged in with AnonymousUser
    def setUp(self):
        self.factory = RequestFactory()
        request.user = AnonymousUser()

    '''
    Create a test to check for a successful GET request of the Edu index view for an anonymous user.
    '''
    def test_index_view(self):
        # create questions for testing
        # use a for loop to create 5 questions as the view cutoff is [:5]
        for i in range(1,6):
            Question.objects.create(question_text=f"Question {i+1}", pub_date=timezone.now())

        # create an instance of index_edu view
        # test index view as if it were deployed at /edu_quiz/edu_quiz.html but i left it as / since not using urls.py in test + no computation for index_edu        
        request = self.factory.get(reverse('Education:index_edu'))
        
        # Simulate an anonymous user because Edu is accessible to unauthenticated users
        request.user = AnonymousUser()

        # simulate a request to index_edu view and capture the resulting HTTP response
        response = views.index_edu(request)

        # assert that the HTTP response status code is 200 (OK), indicating a successful request.
        self.assertEqual(response.status_code, 200, 'Should check for a successful GET request of index view for anyone')
        
        # comment out logging after debugging
        # Add the following line to print to the console
        # logging.basicConfig(level=logging.DEBUG)

        # comment out logging
        # Log the content of the response
        # logging.debug(response.content.decode())

        # assert that the rendered HTML contains the content from the latest questions
        # note the range isn't (5) because it gave an error saying Question wasn't there
        # after importing logging to print the view response to cmd, (2,6) printed Q 2-6 & passed the test
        for i in range(2,6):
            self.assertContains(response, f"Question {int(i)}", msg_prefix="Should check that the last 5 questions are list.")

    '''
    Display a message if there are no questions for Education.
    '''
    # https://docs.djangoproject.com/en/5.0/intro/tutorial05/#id8
    def test_no_questions(self):        
        # create an instance of the client
        client = Client()        

        # assert there are no questions in database
        self.assertEqual(Question.objects.count(), 0)

        #
        # assert ...
        # note assertQuerysetEqual for django version 3.2 instead of assertQuerySetEqual for django version 1.7 like
        response = self.client.get(reverse("Education:index_edu"))
        self.assertEqual(response.status_code, 200, msg= "Check that the server received the request")
        self.assertContains(response, "No quizzes are available.", msg_prefix='Should give a response that there are no quizzes')
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    '''
    Create a test to check for a successful GET request of the Edu detail view for an anonymous user.
    '''
    # ...
    # https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#example
    def test_detail_view(self):        
        # create an instance of detail view
        # test detail view as if it were deployed at /edu_quiz/edu_quiz.html
        # place any number for id
        # Assert that the HTTP response status code is 200 (OK), indicating a successful request.
        question = Question.objects.create(question_text="Sample Question", pub_date=timezone.now())
        question_id = question.id        
        request = self.factory.get("/{question_id}/")
        response = views.detail(request, question_id=question_id)
        self.assertEqual(response.status_code, 200, 'Should check for a successful GET request of detail view for anyone')

    '''
    Create a test that checks if the detail view will render with the correct question id.
    '''
    # Create a test that checks if the detail view will render with the correct question id
    def test_valid_id_for_detailview(self):
        # create a Question instance for testing.
        question = Question.objects.create(question_text='Test Question', pub_date = timezone.now())

        # create an instance of a GET request.
        # question_id as a keyword argument to the reverse function, to match the URL pattern in Edu app's urls.py
        request = self.factory.get(reverse('Education:detail', kwargs={'question_id':question.id}))

        # simulate an anonymous user.
        request.user = AnonymousUser()

        # call the detail view with the request
        response = views.detail(request, question_id=question.id)

        # use get_object_or_404 to ensure the Question exists because the object is expected to exist
        question_from_db = get_object_or_404(Question, pk=question.id)

        # assert that the HTTP response status code is 200 (OK), indicating a successful request
        # assert that the question text attribute is in the response
        # assert that the whole question object passed to the template context in the response is identical to the one retrieved from the database
        self.assertEqual(response.status_code, 200,
                          "Should check for a successful GET request of detail view with correct question_id")
        self.assertEqual(question_from_db.question_text, 'Test Question',
                          msg_prefix='Should check that the question text is in the detail view response')
        self.assertEqual(response.context['question'], question_from_db,
                          msg_prefix='Should check that question object passed to the template matches that in the database')

    '''
    '''
    #
    def test_invalid_id_for_detailview(self):
        # set an invalid question id
        invalid_question_id = 2373

        # create an instance of a GET request
        # question_id is a keyword argument to the reverse function, to match the URL pattern in Edu app's urls.py
        request = self.factory.get(reverse('Education:detail', kwargs={'question_id':invalid_question_id}))

        # simulate an anonymous user
        request.user = AnonymousUser()

        # assert that an error raises if a request is made for an invalid id
        # when testing an invalid ID, the expected behavior is a Http404 exception
        with self.assertRaises(Http404):
            views.detail(request, question_id=invalid_question_id)


    def test_past_questions(self):
        '''
        Display text of question detail view.
        '''
        #https://docs.djangoproject.com/en/3.2/intro/tutorial05/#id10
        # Create a question for testing
        past_question = Question(question_text='Past Question.', days=-5)

        # Create a request with the URL for the past question
        url = reverse('Education:detail', args=(past_question.id,))
        request = self.factory.get(url)

        # Call the detail view with the request
        response = views.detail(request, question_id=past_question.id)

        # Check if the response contains the past question's text
        self.assertContains(response, past_question.question_text)

    '''
    '''
    #
    def test_results_view_with_valid_id(self):     
        # create a Question instance for testing.
        question = Question.objects.create(question_text='Test Question', pub_date = timezone.now())

        # create an instance of a GET request.
        # question_id as a keyword argument to the reverse function, to match the URL pattern in Edu app's urls.py
        request = self.factory.get(reverse('Education:results', kwargs={'question_id':question.id}))

        # simulate an anonymous user.
        request.user = AnonymousUser()

        # call the detail view with the request
        response = views.results(request, question_id=question.id)

        # use get_object_or_404 to ensure the Question exists because the object is expected to exist
        question_from_db = get_object_or_404(Question, pk=question.id)

        # assert that the HTTP response status code is 200 (OK), indicating a successful request        
        # assert that the whole question object passed to the template context in the response is identical to the one retrieved from the database
        self.assertEqual(response.status_code, 200,
                          "Should check for a successful GET request of results view with correct question_id")        
        self.assertEqual(response.context['question'], question_from_db,
                          msg_prefix='Should check that question object passed to the template matches that in the database')

    def test_results_view_with_invalid_id(self):     
        pass
    #def test_vote_view(self):
        # pass