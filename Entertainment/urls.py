from django.urls import path
from . import views

app_name = 'Entertainment'

urlpatterns = [
    path('', views.entertainment_page, name='Entertainment page'), 
]