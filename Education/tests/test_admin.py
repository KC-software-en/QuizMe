# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
from django.test import TransactionTestCase

# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#adminsite-objects
# register your model instances with site object
# The site object is an instance of the AdminSite class and represents the default admin site for your Django project
from django.contrib.admin.sites import site

# import admin.py
from .. import admin

# import the question & choice models
from ..models import Question, Choice

######################################################################################################
######################################################################################################

'''
Create a class to test the model registration on the Admin site.
'''
# test that the models were registered on admin site
class TestModelRegistration(TransactionTestCase):
    '''
    Create a method to test the Question model registration.
    '''
    # assert that question model was registered with the admin site
    # - by examining the internal attribute of the AdminSite class in Django - the _registry attribute of the site object.
    # _registry is a dictionary where {model classes:admin classes associated with those models}
    def test_question_registration(self):
        self.assertIn(Question,site._registry, 'Should check Question is on the admin site')
    
    '''
    Create a method to test the Choice model registration.
    '''
    # assert that Choice model was registered with the admin site
    def test_choice_registration(self):
        self.assertIn(Choice, site._registry, 'Should check Choice is on the admin site')
    