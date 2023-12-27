from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Home.views import index

class TestUrls(SimpleTestCase):

    def test_home_page(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func, index)