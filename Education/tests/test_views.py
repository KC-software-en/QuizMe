# https://docs.djangoproject.com/en/5.0/intro/tutorial05/#id7
# reverse function is used in Django to generate URLs for views based on their names or patterns
from re import U
from urllib import request, response
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
    # setup RequestFactory for all views
    # setup a user who is not logged in with AnonymousUser
    def setUp(self):
        self.factory = RequestFactory()
        request.user = AnonymousUser()

    def test_index_view(self):
        # create an instance of index view
        # test index view as if it were deployed at /edu_quiz/edu_quiz.html but i left it as / since not using urls.py in test + no computation for index_edu
        # Assert that the HTTP response status code is 200 (OK), indicating a successful request.
        request = self.factory.get('/')
        response = views.index_edu(request)
        self.assertEqual(response.status_code, 200, 'Should check for a successful GET request of index view for anyone')

    # https://docs.djangoproject.com/en/5.0/intro/tutorial05/#id8
    def test_no_questions(self):
        '''
        Display a message if there are no questions
        '''
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

    #def test_results_view(self):
     #   pass

    #def test_vote_view(self):
     #   pass