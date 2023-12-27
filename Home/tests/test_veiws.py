from django.test import TestCase
from Home.views import index

class HomeViewTest(TestCase):
    def test_view_using_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'Home page.html')