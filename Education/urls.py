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
# include the category id from the json response of trivia categories on open trivia db
urlpatterns = [
    path('', views.index, name='index'),    
    path('Education/<int:category_id>/', views.index_edu, name='index_edu'),   
    path('Education/<int:quantity>/<int:category>/MythologyQuiz/', views.get_questions_and_choices, name='detail'),              
    path('Education/MythologyQuiz/selection/', views.selection, name='selection'),    
    path('Education/MythologyQuiz/results/<int:result>/<int:question_quantity>', views.results, name='results')
    
]
