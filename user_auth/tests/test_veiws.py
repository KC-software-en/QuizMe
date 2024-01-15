# Django documentation.
#https://docs.djangoproject.com/en/4.2/topics/testing/advanced/

# Import The request factory. 
# RequestFactory provides a way to generate a request instance that can be used as the first argument to any view.
# Import TestCase.
# TestCase is a set of actions executed to verify a particular functionality.
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
# import views.
from .. import views
'''
Create a class to test the use_auth views.
'''
# The test will fail as the user_login view is used as an inccorect template to render then home page it should use the Home page.html string as an assertion templatename.  
class UserAuthViewTest(TestCase):
    '''
        A function to test if the correct template is rendered from the login view.
    '''               
    # Positive tests "If the correct template is used (login.html)"
    def test_login_view_valid(self):
        # Create an instance of a GET request.
        req = RequestFactory().get('/user_auth/login')
        # Check if the template can be accessed through the user_login view. 
        resp = views.user_login(req)
        # The test will pass as the Index view is not rendered in the /user_auth/login url.      
        assert resp.status_code == 200 , 'The login page should be rendered to anyone '           

    '''
        A function to test if the correct template is rendered from the logout view.
    '''
    # Positive tests "If the correct template is used (logout.html)"
    def test_logout_view_valid(self):
        # Create an instance of a GET request.
        req = RequestFactory().get('/user_auth/logout')
        # Check if the template can be accessed through the user_logout view. 
        resp = views.user_logout(req)
        # The test will pass as the Index view is not rendered in the /user_auth/logout url.      
        assert resp.status_code == 200 , 'The logout page should be rendered to anyone '  

    '''
        A function to test if the correct template is rendered from the register view.
    '''       
   # Positive tests "If the correct template is used (register.html)"
    def test_register_view_valid(self):
        # Create an instance of a GET request.
        req = RequestFactory().get('/user_auth/register')
        # Check if the template can be accessed through the user_register view. 
        resp = views.user_register(req)
        # The test will pass as the Index view is not rendered in the /user_auth/register url.      
        assert resp.status_code == 200 , 'The register page should be rendered to anyone '
