"""
This module contains the NewUserForm class, which is used to create a form where the user can register.

The NewUserForm class inherits from the UserCreationForm class and overrides the save method to set the email field of the user instance to the value of the cleaned_data['email'] field.

The NewUserForm class defines the model and fields attributes to correspond to the User model and the fields that should be included in the form.

The save method of the NewUserForm class first calls the super().save() method to create the user instance, and then sets the email field of the user instance to the value of the cleaned_data['email'] field. If the commit parameter is set to True, the user instance is saved to the database.

The NewUserForm class is used in the views.py module to create the form for registering a new user.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# https://www.pythontutorial.net/django-tutorial/django-registration/¹ 
class NewUserForm(UserCreationForm):
    """
    This class defines the NewUserForm, which is used to create a form where the user can register.
    """
    email = forms.EmailField(required=True)

    class Meta:
        """
        This class defines the Meta class for the NewUserForm class, which specifies the model and fields attributes to correspond to the User model and the fields that should be included in the form.
        """
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """
        Overrides the save method of the UserCreationForm class to set the email field of the user instance
        to the value of the cleaned_data['email'] field.

        :param commit: A boolean value indicating whether to save the user instance to the database.
        :type commit: bool
        :return: A user instance.
        :rtype: form
        """
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user