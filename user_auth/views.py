from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def user_login(request):
    """
    Renders the login.html template for user login.
    
    request: The HTTP request object.
        
    Returns: A rendered HTML page for user login.
    """
    return render(request, "login.html")


# This veiw logs the user out.
def user_logout(request):
    """
    Logs out the user and displays a success message.

    request: The HTTP request object.

    Returns: A rendered response with the 'logout.html' template.
    """
    logout(request)
    messages.success(request, ("You were successfully logged out."))
    return render(request, 'logout.html')


# This veiw is used to register a new user.
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

            user = User.objects.create_user(username=username, email=email, password=password )
            send_mail(
                subject=f"Welcome {username} to QuizMe",
                message="We are glad that you have registered to our quiz website fellow quizee.",
                from_email="QuizMe2024@gmail.com",
                recipient_list=[user.email],
                fail_silently=True,
            )
            user.save()
            messages.success(request, "Registration successful."),
            storage = get_messages(request)
            for message in storage:
                return redirect("user_auth:login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
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
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponseRedirect(reverse("user_auth:login"))
    else:
        login(request, user)
    return HttpResponseRedirect(reverse("user_auth:show_user"))

@login_required(login_url='user_auth:login')
def show_user(request):
    """
    Displays user information.

    request: (HttpRequest): The HTTP request object.

    Returns: HttpResponse: Rendered template with user data (username and password).
    """
    print(request.user.username)
    return render(request, 'user.html', {
        "username": request.user.username,
        "password": request.user.password
})

