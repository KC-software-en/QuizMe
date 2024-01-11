# create urls.py in the directory of the education app

# import path to map a URL to a specific view function in Django
# import include to use other URL patterns from other modules (apps)
from django.urls import path, include

# import views which contain the functions or classes responsible for handling HTTP requests
# and returning appropriate responses, rendering web pages.
from . import views

#############################################################################################
#############################################################################################

# add an app_name to set the application namespace
app_name = 'Education'

# under urlpatterns, paste the code that references the functions in views.py
urlpatterns = [
    path('', views.index, name='index'),    
    path('index_edu/', views.index_edu, name='index_edu'),        
    path('<int:question_id>/',views.detail, name='detail'),
    path('<int:question_id>/results/',views.results, name='results'),
    path('<int:question_id>/vote/',views.vote, name='vote'),
]
