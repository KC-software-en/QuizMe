from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

# NewUserForm used to create a form where the user can register.
class NewUserForm(UserCreationForm):
	first_name = forms.CharField(max_length=5000)

	class Meta:
		model = User
		fields = ("username", "first_name", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		if commit:
			user.save()
		return user