from django.test import TestCase
from user_auth.views import user_login, user_logout, user_register

# Failing tests "If the incorrect template is used"
class UserAuthViewTest(TestCase):
    def test_login_view_using_template(self):
        response = self.client.get('login/') # Get the ('login) url path as a client.  
        self.assertTemplateUsed(response, user_login) # Check if the template can be accessed through the user_login veiw.
        # The test will fail as the user_login view is used as an inccorect template to render then home page it should use the Home page.html string as an assertion templatename.    

    def test_logout_view_using_template(self):
            response = self.client.get('logout') # Get the ('logout') url path as a client.  
            self.assertTemplateUsed(response, user_logout) # Check if the template can be accessed through the user_logout view.    
        # The test will fail as the user_logout view is used as an inccorect template to render then logout page it should use the logout.html string as an assertion templatename.
            
    def test_register_view_using_template(self):
            response = self.client.get('register') # Get the ('register') url path as a client.  
            self.assertTemplateUsed(response, user_register) # Check if the template can be accessed through the user_register view.    
        # The test will fail as the user_register view is used as an inccorect template to render then register page it should use the register.html string as an assertion templatename.

# Positive tests "If the correct template is used"   
                        
    def test_login_view_using_template(self):
        response = self.client.get('/user_auth/login') # Get the ('login) url path as a client.  
        self.assertTemplateUsed(response,'login.html') # Check if the login.html template can be accessed.
        # The test will fail as the user_login view is used as an inccorect template to render then home page it should use the Home page.html string as an assertion templatename.    

    def test_logout_view_using_template(self):
            response = self.client.get('/user_auth/logout') # Get the ('logout') url path as a client.  
            self.assertTemplateUsed(response, 'logout.html') # Check if the logout.html template can be accessed.    
        # The test will fail as the user_logout view is used as an inccorect template to render then logout page it should use the logout.html string as an assertion templatename.
            
    def test_register_view_using_template(self):
            response = self.client.get('/user_auth/register') # Get the ('register') url path as a client.  
            self.assertTemplateUsed(response, 'register.html') # Check if the register.html template can be accessed.    
        # The test will fail as the user_register view is used as an inccorect template to render then register page it should use the register.html string as an assertion templatename.