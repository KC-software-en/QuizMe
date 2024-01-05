from django.test import TestCase
from ..forms import NewUserForm
from django.urls import reverse

# Failing test ifform is invalid
class TestAccountCreationForm(TestCase):
    def test_signup_form_invalid(self):
        form = NewUserForm(data={})

        # It creates a dummy user/form and checks if the form is valid and that their is no errors in this case the form is not valid as it is empty.
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

# Positive test if form is valid        
    def test_signup_form(self):
        form = NewUserForm(data={
            'username': 'Jeffrey',
            'first_name': 'Junior',
            'password1': 'Jeffjun2@',
            'password2': 'Jeffjun2@'
        })
        # It creates a dummy user/form and checks if the form is valid and that their is no errors in this case the form has valid data.

        self.assertTrue(form.is_valid())
        