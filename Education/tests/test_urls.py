# Django documentation.
#https://docs.djangoproject.com/en/5.0/topics/testing/tools/#simpletestcase

# Import SimpleTestCase.
# This helps to avoid executing write queries which will affect other tests since each SimpleTestCase test isn’t run in a transaction.
from django.test import SimpleTestCase
# Import reverse is a utility function in Django that is used to generate URLs for views from their names and arguments
# Import resolve which is used to resolve URL paths to a corresponding view.
from django.urls import reverse, resolve
# Import views.
from .. import  views

'''
Create a class to test the Urls.
''' 
# Create a failing test.
# After writing the fail test, run in cmd terminal it should fail. 
# Next, go to views.py and create the index view and it should pass.
# Create a class to test the home views.
# run coverage after tests
class TestUrls(SimpleTestCase):

    def setup(self):
        # no necessary conditions
        pass    

    '''
        A function to test if the correct template is rendered if the user enters the home url path.
    '''    
    # The test below will pass because the resolver match returns an index view and not the string 'index'.
    def test_home_page_valid(self):
        # Used to generate a Url based on the view name.
        url = reverse('Education:index')     
        # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw.        
        self.assertEquals(resolve(url).func, views.index) 
        