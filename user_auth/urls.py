"""
This file contains the URL patterns for the user authentication app.
"""
from django.urls import path
from user_auth import views

app_name = 'user_auth'
urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('register/', views.user_register, name="register"),
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    path('authenticate_user/show_user', views.show_user, name='show_user'),  # The url path to user page.

]
