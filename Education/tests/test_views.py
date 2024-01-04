# https://docs.djangoproject.com/en/5.0/intro/tutorial05/#id7
# reverse function is used in Django to generate URLs for views based on their names or patterns
from django.urls import reverse

# import views
from .. import views

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
from django.test import TransactionTestCase

#############################################################################################
#############################################################################################

'''
Create a class to test the behaviour of a view associated with the "index" endpoint of a education app.
'''
# Create a class to test the index view
class QuestionIndexViewTests(TransactionTestCase):
    def test_no_questions(self):
        """
        A method responsible for testing a specific scenario related to the absence of questions.
        """
        # Send a GET request to the "index" endpoint using Django's client object
        # use reverse("Education:index") to generate the URL for the "index" endpoint based on its name
        # Assert that the HTTP response status code is 200 (OK), indicating a successful request.
        # Assert that the response body contains the specified text, indicating that there are no questions available
        # If no questions exist, an appropriate message is displayed.
        # Assert that the "latest_question_list" in the context of the response is an empty queryset, indicating that no questions are present
        response = self.client.get(reverse("Education:index"))
        self.assertEqual(response.status_code, 200, 'Should check for a successful GET request')        
        self.assertContains(response, "No questions are available.", 'Should check that a message displays if no questions exist')
        self.assertQuerySetEqual(response.context["latest_question_list"], [], 'Should check that no questions are present')       