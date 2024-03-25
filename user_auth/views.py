### Documentation used to construct the user_auth views for user authentification. ###
# https://docs.djangoproject.com/en/5.0/ref/contrib/messages/
# https://docs.djangoproject.com/en/5.0/topics/auth/default/
# https://docs.djangoproject.com/en/5.0/topics/email/
# https://www.pythontutorial.net/django-tutorial/django-registration/

### import all the required imports for the views to work. ###
# Import render and redirect from django.shortcuts.
from django.shortcuts import render, redirect
# Importing the NewUserForm from .forms module.
from .forms import NewUserForm
# Import the User model from django.contrib.auth.models.
from django.contrib.auth.models import User
# Import authentication functions from Django's contrib.auth module.
from django.contrib.auth import authenticate, login, logout
# Redirects the user to a specific URL using HttpResponseRedirect.
from django.http import HttpResponseRedirect
# Reverse is used to dynamically generate URLs based on view names.
from django.urls import reverse
# Import the messages framework from Django for displaying flash messages.
from django.contrib import messages
# Import the send_mail function from django.core.mail.
from django.core.mail import send_mail
# Import the get_messages function from django.contrib.messages.
from django.contrib.messages import get_messages
# Ensures that the user is logged in before accessing the view.
from django.contrib.auth.decorators import login_required


# Create your views here.
# user_login view.
def user_login(request):
    """
    Renders the login.html template for user login.
    
    request: The HTTP request object.
        
    Returns: A rendered HTML page for user login.
    """
    # Renders the login template.
    return render(request, "login.html")


# This veiw logs the user out.
def user_logout(request):
    """
    Logs out the user and displays a success message.

    request: The HTTP request object.

    Returns: A rendered response with the 'logout.html' template.
    """
    # Deletes the users session.
    logout(request)
    # Message is displayed once the user loggs out.
    messages.success(request, ("You were successfully logged out."))
    return render(request, 'logout.html')


# This view renders the logged in user information.
@login_required(login_url='user_auth:login')
def show_user(request):
    """
    Displays user information.

    request: (HttpRequest): The HTTP request object.

    Returns: HttpResponse: Rendered template with user data (username and password).
    """
    # Renders the users information into the template.
    print(request.user.username)
    return render(request, 'user.html', {
        "username": request.user.username,
        "password": request.user.password
})


# This veiw is used to register a new user.
# Once the user succesfully registers on the website they are automatically sent an email.
def user_register(request):
    """
    Handles user registration.

    request: The HTTP request object.

    Returns: If successful, redirects to the login page.
             If unsuccessful, displays an error message and renders the registration form.
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)        
        if form.is_valid():            
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password1"]

            # Creates the user.
            user = User.objects.create_user(username=username, email=email, password=password )
            # Once the users are created the email gets sent to the email that has been used to register.
            send_mail(
                subject=f"Welcome {username} to QuizMe",
                message="We are glad that you have registered to our quiz website fellow quizee.",
                from_email="QuizMe2024@gmail.com",
                recipient_list=[user.email],
                fail_silently=True,
            )
            # Once the email has been sent the user is then saved i the database.
            user.save()
            # This message then gets rendered confiming the registration.
            messages.success(request, "Registration successful."),
            storage = get_messages(request)
            # If there is no errors the user is then redirected to the login page.
            for message in storage:
                return redirect("user_auth:login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    # The form data gets erased and replaced with a new form.    
    form = NewUserForm()
    return render(
        request=request, template_name="register.html", context={"register_form": form}
    )


#  This veiw is used to authenticate and check if the user already exists.
def authenticate_user(request):
    """
    Authenticates a user based on the provided username and password.

    request: The HTTP request object containing POST data.

    Returns: If authentication is successful, redirects to the "show_user" page.
             If authentication fails, redirects to the "login" page.
    """
    # Compares the data login  to the data in the database to see if they are simillar.
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    # If there is no user in the database that matches the data in the database they are redirected to the login page to try again.
    if user is None:
        return HttpResponseRedirect(reverse("user_auth:login"))
    # If the user enters the correct data they are then logged in and redirected to the show_user view.
    else:
        login(request, user)
        return HttpResponseRedirect(reverse("user_auth:show_user"))

