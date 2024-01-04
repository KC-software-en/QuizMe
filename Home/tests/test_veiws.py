from django.test import TestCase
from Home.views import index

# Failing test 
class HomeViewTest(TestCase):
    def test_view_using_template(self):
        response = self.client.get('/') # Get the ('/') url path as a client.        
        self.assertTemplateUsed(response, index) # Check if the template can be accessed through the index view.        
        # The test will fail as the Index view is used as an inccorect template to render then home page it should use the Home page.html string as an assertion templatename.
        
# Positive test  
    def test_view_using_template(self):
        response = self.client.get('/') # Get the ('/') url path as a client.        
        self.assertTemplateUsed(response, 'index.html')  # Check the Home page.html template can be rendered as a response.
        # The test will pass as the Home page.html string is used as an assertion templatename.