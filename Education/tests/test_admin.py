# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
from django.test import TransactionTestCase

# import mixer
# The Mixer is a helper to generate instances of Django or SQLAlchemy models. 
# It’s useful for testing and fixture replacement
from mixer.backend.django import mixer

# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#adminsite-objects
# register your models and ModelAdmin instances with AdminSite
from django.contrib.admin.sites import AdminSite

# import admin.py
from .. import admin

# import the question & choice models
from .. import models

#
from django.urls import reverse

######################################################################################################
        
'''
Create a class to test the Question model in Admin.py.
'''
# create a class to test the Question model in Admin.py
class TestQuestionAdmin(TransactionTestCase):
    def setUp(self):
        '''
        Setup the AdminSite for the Question testing in admin.
        '''
        # Create an instance of the AdminSite
        self.site = AdminSite()

    '''
    Create a method to test interactions the Question instances have with the Django admin interface.'''
    # test interactions with the Django admin interface, simulating changes to model instances through the admin site.
    def test_question_admin(self):
        # Create a Question instance using mixer
        question_instance = mixer.blend(Question, question_text='Will this question show my educational future?')

        # Create an instance of the Question Admin
        question_admin = Question(Question, self.site)

        # assert that the list_display attribute is set correctly
        self.assertEqual(question_admin.list_display, ('question_text', 'pub_date'), 'Should confirm Question list_display attribute was created correctly')

        # Simulate displaying the change page for the question
        # (when you click on an instance in the list_view of admin site, it takes you to the page where you can 'change' the values for each field e.g. form fields)
        # use reverse function to help you generate a URL dynamically based on the app name and model name
        # admin indicates that the subsequent path is part of the Django admin site
        # question_instance.id is used as an argument to specify which instance of the Question model you want to view/edit
        change_url = reverse('admin:Education_question_change', args=[question_instance.id])
        response = self.client.get(change_url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200, 'Should check that the admin change page is accessible via server')

        # Simulate posting a form to change the question's text
        # create a dictionary named data containing the data that you want to submit in the form
        # i.e. new value for the question_text field.         
        # use Django test client to simulate a POST request to the URL specified by change_url with the form data
        # response variable holds the server's response to this simulated form submission
        data = {'question_text': 'Updated question text'}
        response = self.client.post(change_url, data)

        # Check that the response status code is a redirect (302)
        # assert that the server should redirect the client to another page after submitting the form
        self.assertEqual(response.status_code, 302, 'Should check that the client redirects to another page after form submission')

        # Check that the question text has been updated in the database
        # query the database to retrieve the Question instance with the same id as question_instance.id.
        # assert that the question_text attribute of the updated Question instance matches the expected value ('Updated question text').
        updated_question_instance = Question.objects.get(id=question_instance.id)
        self.assertEqual(updated_question_instance.question_text, 'Updated question text', 
                         'Should check the database was successfully updated with the new question text submitted through the form')

'''
Create a class to test the Choice model in Admin.py.
'''
# create a class to test the Choice model in Admin.py
class TestChoiceAdmin(TransactionTestCase):    
    def setUp(self):
        '''
        Setup the AdminSite for the Question testing in admin.
        '''
        # Create an instance of the AdminSite
        self.site = AdminSite()

    '''
    Create a method to test interactions the Choice instances have with the Django admin interface.
    '''
    def test_choice_admin(self):
        # Create a Choice instance using mixer
        choice_instance = mixer.blend(Choice, choice_text='Option 1')

        # Create an instance of the Choice Admin
        choice_admin = Choice(Choice, self.site)

        # assert that the list_display attribute is correct
        self.assertEqual(choice_admin.list_display, ('choice_text', 'votes'), 'Should confirm Choice list_display attribute was created correctly')

        # Simulate displaying the change page for the choice
        # use reverse function to help you generate a URL dynamically based on the app name and model name
        # admin indicates that the subsequent path is part of the Django admin site
        # choice_instance.id is used as an argument to specify which instance of the Choice model you want to view/edit
        change_url = reverse('admin:Education_choice_change', args=[choice_instance.id])
        response = self.client.get(change_url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200, 'Should check that the admin change page is accessible via server')

        # Simulate posting a form to change the choice's text
        # create a dictionary named data containing the data that you want to submit in the form
        # i.e. new value for the choice_text field.         
        # use Django test client to simulate a POST request to the URL specified by change_url with the form data
        # response variable holds the server's response to this simulated form submission
        data = {'choice_text': 'Updated Option 1'}
        response = self.client.post(change_url, data)

        # Check that the response status code is a redirect (302)
        # assert that the server should redirect the client to another page after submitting the form
        self.assertEqual(response.status_code, 302, 'Should check that the client redirects to another page after form submission')

        # Check that the choice text has been updated in the database
        # query the database to retrieve the Choice instance with the same id as choice_instance.id.
        # assert that the choice_instance attribute of the updated Choice instance matches the expected value ('Updated choice text').
        updated_choice_instance = Choice.objects.get(id=choice_instance.id)
        self.assertEqual(updated_choice_instance.choice_text, 'Updated Option 1', 'Should check the database was successfully updated with the new choice text submitted through the form')
