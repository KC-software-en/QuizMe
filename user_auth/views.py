### Documentation used to construct the user_auth views for user authentification. ###
# https://docs.djangoproject.com/en/5.0/ref/contrib/messages/
# https://docs.djangoproject.com/en/5.0/topics/auth/default/
# https://docs.djangoproject.com/en/5.0/topics/email/
# https://mailtrap.io/blog/django-send-email/
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
    Renders the login template.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The rendered login template.
    :rtype: HttpResponse
    """
    # Renders the login template.
    return render(request, "login.html")


# This veiw logs the user out.
def user_logout(request):
    """
    Logs out the user by deleting the session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response with a success message and the "logout.html" template.
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
    Renders the user's information into the template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the rendered user information in the 'user.html' template.
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
    View function to handle user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The response containing the registration form or redirecting to the login page.

    Raises:
        None

    Example:
        To register a new user, make a POST request with valid form data.
        If successful, the user will receive a welcome email and be redirected to the login page.
        If unsuccessful, an error message will be displayed.
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
    Authenticates a user based on the provided login data.

    Args:
        request (HttpRequest): The HTTP request object containing POST data.

    Returns:
        HttpResponseRedirect: Redirects the user to the login page if authentication fails,
        or to the show_user view if authentication succeeds.
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

