from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_auth.views import user_login, user_logout, user_register

# Failing test "If the user is directed to the wrong url"
class TestUrls(SimpleTestCase):

    def test_login_page(self):
        url = reverse("login") # used to generate a URL based on view name.
        self.assertEquals(resolve(url).func, 'user_login') # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw and not a string.
        # The above Testing class will fail because the resolver match should return the user_login view and not the string 'user_login'.

    def test_logout_page(self):
        url = reverse("logout") # used to generate a URL based on view name.
        self.assertEquals(resolve(url).func, 'user_logout') # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw and not a string.
        # The above Testing class will fail because the resolver match should return the user_logout view and not the string 'user_logout'.

    def test_register_page(self):
        url = reverse("register") # used to generate a URL based on view name.
        self.assertEquals(resolve(url).func, 'user_register') # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw and not a string.
        # The above Testing class will fail because the resolver match should return the user_register view and not the user_register 'index'.   

# Positive test "If the user is directed to the correct url"
        
    def test_login_page(self):
        url = reverse("login") # used to generate a URL based on view name.
        self.assertEquals(resolve(url).func, user_login) # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw.
        # The above Testing class will Pass because the resolver match should return the user_login view.

    def test_logout_page(self):
        url = reverse("logout") # used to generate a URL based on view name.
        self.assertEquals(resolve(url).func, user_logout) # The assert equals function is used to take the url path and return a object based on the resolver match which is a view.
        # The above Testing class will Pass because the resolver match should return the user_logout view.

    def test_register_page(self):
        url = reverse("register") # used to generate a URL based on view name.
        self.assertEquals(resolve(url).func, user_register) # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw.
        # The above Testing class will Pass because the resolver match should return the user_register view.