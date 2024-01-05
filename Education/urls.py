# create urls.py in the directory of the education app

# import path
# import views
from operator import index
from django.urls import path, include
from . import views

#############################################################################################
#############################################################################################

# add an app_name to set the application namespace
app_name = 'Education'

# under urlpatterns, paste the code that references the index function in views.py
urlpatterns = [
path('', views.index, name='index'),
]
