# Django documentation.
# https://docs.djangoproject.com/en/4.2/topics/testing/advanced/
# https://stackoverflow.com/questions/3728528/testing-email-sending-in-django
# https://mailtrap.io/blog/django-send-email/

# Import The request factory. 
# RequestFactory provides a way to generate a request instance that can be used as the first argument to any view.
# Import TestCase.
# TestCase is a set of actions executed to verify a particular functionality.
import unittest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.test import Client
from django.contrib.messages import get_messages
from user_auth.views import authenticate_user
# import views.
from .. import views
  
class UserAuthViewTest(TestCase):
    '''
        Create a class to test the login, logout and show user view in the user_auth views.
    '''                  
    # Positive tests "If the correct template is used (login.html)"
    def test_login_view_valid(self):
        '''
            A function to test if the correct template is rendered from the login view.
        ''' 
        # Create an instance of a GET request.
        req = RequestFactory().get('/user_auth/login')
        # Check if the template can be accessed through the user_login view. 
        resp = views.user_login(req)
        # The test will pass as the Index view is not rendered in the /user_auth/login url.      
        assert resp.status_code == 200 , 'The login page should be rendered to anyone '           

    # Positive tests "If the correct template is used (logout.html)"
    def test_logout_view_valid(self):
        '''
            A function to test if the correct template is rendered from the logout view.
        '''
        # Create an instance of a GET request.
        resp = self.client.get(reverse('user_auth:logout'))
        # The test will pass as the url is rendered at the /user_auth/login url       
        assert resp.status_code == 200 , 'The logout page should be rendered to anyone '  

    # Positive tests "If the correct template is used (show_user.html) and it displays the signed in user details."      
    def test_show_user(self):
        '''
            A function to test if the correct template is rendered from the show_user view.
        ''' 
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass')
        self.url = reverse('user_auth:show_user')

        request = self.factory.get(self.url)
        request.user = self.user
        response = views.show_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)    

class test_user_register_view(TestCase):
        '''
                A class with functions to test the user_register_view.
        '''       
   # Positive tests "If the correct template is used (register.html)"
        def test_register_view_valid(self):
            '''
                A function to test if the correct template is rendered from the register view.
            ''' 
            # Create an instance of a GET request.
            req = RequestFactory().get('/user_auth/register')
            # Check if the template can be accessed through the user_register view. 
            resp = views.user_register(req)
            # The test will pass as the Index view is not rendered in the /user_auth/register url.      
            assert resp.status_code == 200 , 'The register page should be rendered to anyone '

        def test_registration_with_invalid_password(self):
            # Create a new user.        
            '''
                A function to test if a error message is displyed when a user enters invalid data in the register form.
            '''  
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

        def test_registration_successful(self):
            '''
                A function to test if registration is succesful.
            '''  
        # Simulate a POST request with valid form data
            response = self.client.post(reverse("user_auth:register"), {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "securepassword",
                "password2": "securepassword",
            })

            # Check if registration was successful (status code 302 for redirect)
            self.assertEqual(response.status_code, 302)

            # Check if a new user was created
            self.assertTrue(User.objects.filter(username="testuser").exists())

            # You can also check other things like email sending, etc.

        def test_registration_with_invalid_data(self):
            '''
                A function to test if user registers with invalid data.
            '''  
            # Simulate a POST request with invalid form data
            response = self.client.post(reverse("user_auth:register"), {
                "username": "invaliduser",
                "email": "invalid_email",  # Invalid email format
                "password1": "weak",
                "password2": "weak",
            })

            # Check if registration failed (status code 200 for form re-rendering)
            self.assertEqual(response.status_code, 200)

            # Check if error messages are displayed
            self.assertContains(response, "Unsuccessful registration. Invalid information.")    

class test_authenticate_user_view(TestCase):
    '''
            A class with functions to test the authentificate_user view.
    '''  
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testUser", password="testPassword")

    def test_authenticate_user(self):
        '''
            A function to test if a user is authentificated.
        '''  
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        response = self.client.post(reverse('user_auth:authenticate_user'), {'username': 'testuser', 'password': 'testpass'})
        user = authenticate(username='testuser', password='testpass')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user, self.user) 
    
    # Positive tests "If the correct template is used (show_user.html) and it displays the signed in user details."  
    def test_redirect_if_not_authenticated(self):
        '''
            A function to test if a user is not authentificated and redirected to login page.
        ''' 
        # Create an instance of a GET request.
        response = self.client.get(reverse('user_auth:show_user'))
        self.assertRedirects(response, '/user_auth/login/?next=%2Fuser_auth%2Fauthenticate_user%2Fshow_user')

    def test_user_authentication_and_redirection(self):
        '''
                A function to test if a user is redirected after they have been authenticated.
        '''  
        # Create a test client
        client = Client()

        # Log in the test user
        client.login(username="testUser", password="testPassword")

        # Make a request to the show_user view.
        response = client.get(reverse("user_auth:show_user"))

        # Assert that the response status code is 200 (OK)
        self.assertEquals(response.status_code, 200)

        # Assert that the correct template ('user.html') is used
        self.assertTemplateUsed(response, "user.html")
    
    def test_user_not_authenticated_but_redirected(self):
        '''
                A function to test if a if a user is redirected after they have been not been authenticated.
        '''  

        # Make a request to the show_user view.
        response = self.client.get(reverse("user_auth:show_user"))

        # Assert that the response status code is 302 (Redirect)
        self.assertEquals(response.status_code, 302, "Redirects the user if not logged in")

       
class TestAuthenticateUser(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('user_auth.views.authenticate')
    @patch('user_auth.views.login')
    def test_successful_authentication(self, mock_login, mock_authenticate):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'password'})
        mock_user = MagicMock()
        mock_authenticate.return_value = mock_user
        response = authenticate_user(request)
        mock_authenticate.assert_called_once_with(username='testuser', password='password')
        mock_login.assert_called_once_with(request, mock_user)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("user_auth:show_user"))

    @patch('user_auth.views.authenticate')
    def test_failed_authentication(self, mock_authenticate):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'password'})
        mock_authenticate.return_value = None
        response = authenticate_user(request)
        mock_authenticate.assert_called_once_with(username='testuser', password='password')
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("user_auth:login"))

  