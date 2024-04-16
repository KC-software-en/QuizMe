### Documentation used to construct the user_auth views for user authentification. ###
# https://docs.djangoproject.com/en/5.0/topics/auth/default/¹
# https://docs.djangoproject.com/en/5.0/ref/contrib/messages/²
# https://docs.djangoproject.com/en/5.0/topics/email/³
# https://www.pythontutorial.net/django-tutorial/django-registration/¹

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
# https://docs.djangoproject.com/en/5.0/topics/auth/default/¹
def user_login(request):
    """
    Renders the login.html template for user login.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: A rendered HTML page for user login.
    :rtype: HTTPResponse
    """
    # Renders the login template.
    return render(request, "login.html")


# This veiw logs the user out.
#https://docs.djangoproject.com/en/5.0/topics/auth/default/¹ 
def user_logout(request):
    """
    Logs out the user and displays a success message.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: A rendered HTML page for user logout.
    :rtype: HTTPResponse
    """
    # Deletes the users session.
    logout(request)
    # Message is displayed once the user loggs out.
    #https://docs.djangoproject.com/en/5.0/ref/contrib/messages/²  
    messages.success(request, ("You were successfully logged out."))
    return render(request, 'logout.html')


# This view renders the logged in user information.
@login_required(login_url='user_auth:login')
def show_user(request):
    """
    Displays user information.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template with user data (username and password)
    :rtype: HTTPResponse
    """
    # Renders the users information into the template.
    print(request.user.username)
    return render(request, 'user.html', {
        "username": request.user.username,
        "password": request.user.password
})


# This veiw is used to register a new user.
# Once the user succesfully registers on the website they are automatically sent an email.
#https://docs.djangoproject.com/en/5.0/topics/auth/default/¹ 
def user_register(request):
    """
    Handles user registration.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: If successful, redirects to the login page.
             If unsuccessful, displays an error message and renders the registration form.
    :rtype: HTTPResponse
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
            # https://docs.djangoproject.com/en/5.0/topics/email/³
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
            #https://docs.djangoproject.com/en/5.0/ref/contrib/messages/²  
            messages.success(request, "Registration successful."),
            storage = get_messages(request)
            # If there is no errors the user is then redirected to the login page.
            for message in storage:
                return redirect("user_auth:login")
        #Display an error message if the registration is unsuccessful.
        #https://docs.djangoproject.com/en/5.0/ref/contrib/messages/²  
        messages.error(request, "Unsuccessful registration. Invalid information.")
    # The form data gets erased and replaced with a new form.    
    form = NewUserForm()
    return render(
        request=request, template_name="register.html", context={"register_form": form}
    )


#  This veiw is used to authenticate and check if the user already exists.
#https://docs.djangoproject.com/en/5.0/topics/auth/default/¹ 
def authenticate_user(request):
    """
    Authenticates a user based on the provided username and password.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: If authentication is successful, redirects to the "show_user" page.
             If authentication fails, redirects to the "login" page..
    :rtype: HTTPResponse
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

