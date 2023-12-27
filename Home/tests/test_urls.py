from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Home.views import index

# Failing test
class TestUrls(SimpleTestCase):

    def test_home_page(self):
        url = reverse("home") # used to generate a URL based on view name.
        print("Resolve : ", resolve(url))# Print out the resolve URL to terminal.

        self.assertEquals(resolve(url).func, 'index') # The assert equals function is used to take the url path and return a object based on the resolver match which is a srting.
        # The above Testing class will fail because the resolver match should return the index view and not the string 'index'.

# Positive test
    def test_home_page(self):
        url = reverse("home")
        print("Resolve : ", resolve(url)) # Print out the resolve URL to terminal.

        self.assertEquals(resolve(url).func, index) # The assert equals function is used to take the url path and return a object based on the resolver match which is a veiw.
        # The above test will pass because the resolver match returns an index view and not the string 'index'.