from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    """
    A custom form for user registration.

    Inherits from UserCreationForm and adds an email field.

    Attributes:
        email (forms.EmailField): Email field for user registration.
    
    Meta:
        model (User): The User model to be used for registration.
        fields (tuple): Fields to be displayed in the form (username, email, password1, password2).

    Methods:
        save(self, commit=True): Overrides the save method to include email field.
            Args:
                commit (bool, optional): Whether to save the user object to the database. Defaults to True.
            Returns:
                User: The saved user object.
    """
    email = forms.EmailField(required=True)

    class Meta:
        
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """
        Overrides the save method to include email field.

        Args:
            commit (bool, optional): Whether to save the user object to the database. Defaults to True.

        Returns:
            User: The saved user object.
        """
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user