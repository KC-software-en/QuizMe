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

# import the Mythology model
from ..models import Mythology

######################################################################################################
######################################################################################################

'''
Create a class to test the model registration on the Admin site.
'''
# test that the models were registered on admin site
class TestModelRegistration(TransactionTestCase):
    '''
    Create a method to test the Mythology model registration.
    '''
    # assert that Mythology model was registered with the admin site
    # - by examining the internal attribute of the AdminSite class in Django - the _registry attribute of the site object.
    # _registry is a dictionary where {model classes:admin classes associated with those models}
    def test_quiz_registration(self):
        self.assertIn(Mythology, site._registry, 'Should check Mythology is on the admin site')
    
    
    