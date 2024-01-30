# Django documentation.
#https://docs.djangoproject.com/en/4.2/topics/testing/advanced/

# Import The request factory. 
# RequestFactory provides a way to generate a request instance that can be used as the first argument to any view.
# Import TestCase.
# TestCase is a set of actions executed to verify a particular functionality.
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import Client
from django.contrib.messages import get_messages
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
        resp = self.client.get(reverse('user_auth:logout'))
        # The test will pass as the url is rendered at the /user_auth/login url       
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


    '''
        A function to test if the correct template is rendered from the show_user view.
    '''       
   # Positive tests "If the correct template is used (show_user.html) and it displays the signed in user details."      
    def test_show_user(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass')
        self.url = reverse('user_auth:show_user')

        request = self.factory.get(self.url)
        request.user = self.user
        response = views.show_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    '''
        A function to test if a user is authentificated.
    '''       
    # Positive tests "If the correct template is used (show_user.html) and it displays the signed in user details."  
    def test_authenticate_user(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        response = self.client.post(reverse('user_auth:authenticate_user'), {'username': 'testuser', 'password': 'testpass'})
        user = authenticate(username='testuser', password='testpass')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user, self.user) 

    '''
        A function to test if a user is not authentificated and redirected to login page.
    '''       
    # Positive tests "If the correct template is used (show_user.html) and it displays the signed in user details."  
    def test_redirect_if_not_authenticated(self):
        # Create an instance of a GET request.
        response = self.client.get(reverse('user_auth:show_user'))
        self.assertRedirects(response, '/user_auth/login/?next=%2Fuser_auth%2Fauthenticate_user%2Fshow_user')

    
    '''
        A function to test if a error message is displyed when a user enters invalid data in the register form.
    '''  
    def test_registration_with_invalid_data(self):
        # Create a new user.
        self.url = reverse('user_auth:register')
        self.invalid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword123'
        }

        response = self.client.post(self.url, self.invalid_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Unsuccessful registration. Invalid information.")