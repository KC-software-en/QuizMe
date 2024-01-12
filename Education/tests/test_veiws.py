# Django documentation.
#https://docs.djangoproject.com/en/4.2/topics/testing/advanced/

# Import The request factory. 
# RequestFactory provides a way to generate a request instance that can be used as the first argument to any view.
# Import TestCase.
# TestCase is a set of actions executed to verify a particular functionality.
from django.test import RequestFactory, TestCase

# Import views.
from .. import views

'''
Create a class to test the Urls.
''' 
# Create a failing test.
# After writing the fail test, run in cmd terminal it should fail. 
# Next, go to views.py and create the index view and it should pass.
# Create a class to test the home views.
# run coverage after tests
class HomeViewTest(TestCase):

    def setup(self):
        # no necessary conditions.
        pass
    
    '''
        A function to test if the incorrect template is rendered from the view.
    '''
    def test_view_using_template_invalid(self):
        # Create an instance of a GET request.
        req = RequestFactory().get('/')
        # Check if the template can be accessed through the index view. 
        resp = views.index(req)
        # The test will pass as the Index view is not rendered in the / url.      
        assert resp.status_code == 200 , 'Should be rendered to anyone '
