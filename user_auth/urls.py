# create urls.py in the directory of the user_auth app

# import path to map a URL to a specific view function in Django
# import include to use other URL patterns from other modules (apps)
from django.urls import path

# import views which contain the functions or classes responsible for handling HTTP requests
# and returning appropriate responses, rendering web pages.
from . import views

#############################################################################################
#############################################################################################

# add an app_name to set the application namespace

app_name = 'user_auth'

# under urlpatterns, paste the code that references the functions in views.py
urlpatterns = [
    # set a path for the login view
    path('login/', views.user_login, name="login"),
    # set a path for the logout view
    path('logout/', views.user_logout, name="logout"),
    # set a path for the register view
    path('register/', views.user_register, name="register"),
    # set a path for the authenticate user view
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    # set a path for the show user view
    path('authenticate_user/show_user', views.show_user, name='show_user'), 

]
