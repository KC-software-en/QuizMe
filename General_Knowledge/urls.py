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
app_name = 'General_Knowledge'

# under urlpatterns, paste the code that references the functions in views.py
urlpatterns = [
    # set a path for the home view of General Knowledge
    path('General_Knowledge/', views.index_gen, name='index_gen'),   
    # set a path for the detail view
    path('<str:category_name>/<int:question_id>/detail/', views.detail, name='gen_detail'),
    # set a path for the selection view
    path('<str:category_name>/<int:question_id>/selection/', views.selection, name='selection'),    
    # set a path for the results view
    path('<str:category_name>results/', views.results, name='results'),
    # set a path for the start a new quiz view
    path('General_Knowledge/try_new_quiz/', views.try_new_quiz, name='try_new_quiz')    
]
