from django.test import TestCase
from Home.views import index

# Failing test
'''
Create a class to test the Urls.
''' 
class HomeViewTest(TestCase):

    def setup(self):
        # no necessary conditions
        pass
    
    '''
        A function to test if the incorrect template is rendered from the view.
    '''
    def test_view_using_template_invalid(self):
        response = self.client.get('/') 
        # Get the ('/') url path as a client.        
        self.assertTemplateNotUsed(response, index) 
        # Check if the template can be accessed through the index view.        
        # The test will fail as the Index view is used as an inccorect template to render then home page it should use the Home page.html string as an assertion templatename.
        
# Positive test 
    '''
        A function to test if the correct template is rendered from the view.
    ''' 
    def test_view_using_template_valid(self):
        response = self.client.get('/') 
        # Get the ('/') url path as a client.        
        self.assertTemplateUsed(response, 'index.html')  
        # Check the Home page.html template can be rendered as a response.
        # The test will pass as the Home page.html string is used as an assertion templatename.