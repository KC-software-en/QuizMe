from django.test import TestCase
from ..forms import NewUserForm
from django.urls import reverse
from django.core import mail

""" A function to test if the form is invalid if it has no data and gets the error messages."""
# Failing test if form is invalid
class TestAccountCreationForm(TestCase):
    def test_signup_form_invalid(self):
        form = NewUserForm(data={})

        # It creates a dummy user/form and checks if the form is valid and that their is no errors in this case the form is not valid as it is empty.
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)


""" A function to test if the form is valid if it has the correct data and gets no error messages."""
# Positive test if form is valid        
def test_signup_form(self):
    form = NewUserForm(data={
        'username': 'Jeffrey',
        'first_name': 'Junior',
        'email': 'testemail@gmail.com',
        'password1': 'Jeffjun2@',
        'password2': 'Jeffjun2@'
    })
    # It creates a dummy user/form and checks if the form is valid and that their is no errors in this case the form has valid data.

    self.assertTrue(form.is_valid())
        
""" A function to test if the user gets redirected after they register."""        
def test_register_form_redirect(self):
    response = self.client.post(reverse('user_auth:register'), data={
        'username': 'testuser',            
        'first_name': 'Usertest',
        'email': 'testemail@gmail.com',
        'password1': 'password321@1',
        'password2': 'password321@1'
    })
    self.assertEqual(response.status_code, 302)    

""" A Class that has a function to test if the automated email gets sent."""   
class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
            'Register succesfull.', 'Welcome to QuizMe.',
            'Quizme.co@gmail.com', ['test_user@gmail.com'],
            fail_silently=False,
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Register succesfull.')
        self.assertEqual(mail.outbox[0].body, 'Welcome to QuizMe.')

""" A Class that has a function to test if the users data from the form is saved so we can get the users email."""
class NewUserFormTestCase(TestCase):
    def test_save_method(self):
        form_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password1': 'testpass123', 'password2': 'testpass123'}
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'testuser@example.com')        