"""QuizMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import admin to make the Django admin functionality available for use in your Django project
# admin allows administrators to easily add, edit, and delete records from the database
from django.contrib import admin

# import path function to define a URL pattern for the paths to apps 
# alter import to add 'include' to include additional URL patterns within the modules(apps)
from django.urls import path, include

#############################################################################################
#############################################################################################

'''
Add paths for the modules in QuizMe.
'''
# add path for admin
# add paths for the apps created in QuizMe
# edu has index.html so leave path open for it to render when server starts
urlpatterns = [
    path('admin/', admin.site.urls),      
    path('', include("Education.urls"))
    path('user_auth/', include("user_auth.urls")),

]
