# Django documentation.
#https://docs.djangoproject.com/en/5.0/topics/testing/tools/#simpletestcase

# Import SimpleTestCase.
# This helps to avoid executing write queries which will affect other tests since each SimpleTestCase test isn’t run in a transaction.
from django.test import SimpleTestCase
# Import reverse is a utility function in Django that is used to generate URLs for views from their names and arguments
# Import resolve which is used to resolve URL paths to a corresponding view.
from django.urls import reverse, resolve
#Import views.
from .. import views

'''
Create a class to test the Urls.
''' 
# Failing test "If the user is directed to the wrong url"
# After writing the fail tests, run in cmd terminal it should fail. 
# Next, go to urls.py and create the urls and it should pass.
# Create a class to test the home views.
# run coverage after tests
class TestUrls(SimpleTestCase):       
    # The test will Pass because the resolver match should return the user_login view.
    def test_login_page_valid(self):
        '''
            A function to test if the correct template is rendered if the user enters the login url path.
        ''' 
        # used to generate a URL based on view name.
        url = reverse("user_auth:login")
        # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw.
        self.assertEquals(resolve(url).func, views.user_login) 
    
    # The test will Pass because the resolver match should return the user_logout view.
    def test_logout_page_valid(self):
        '''
            A function to test if the correct template is rendered if the user enters the logout url path.
        '''
        # used to generate a URL based on view name.
        url = reverse("user_auth:logout") 
        # The assert equals function is used to take the url path and return a object based on the resolver match which is a view.
        self.assertEquals(resolve(url).func, views.user_logout) 
    
    # The test will Pass because the resolver match should return the user_register view.
    def test_register_page_valid(self):
        '''
            A function to test if the correct template is rendered if the user enters the register url path.
        '''
        # used to generate a URL based on view name.
        url = reverse("user_auth:register") 
        # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw.
        self.assertEquals(resolve(url).func, views.user_register) 
        
        
