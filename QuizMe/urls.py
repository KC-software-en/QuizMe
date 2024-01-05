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
from django.contrib import admin
<<<<<<< Updated upstream
=======
# add ', include' to the import from django.urls
>>>>>>> Stashed changes
from django.urls import path, include

# add the url to the education app
# leave an empty string
urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< Updated upstream
    path('', include('Home.urls')),
    path('user_auth/', include("user_auth.urls")),

=======
    #path('', include('index.urls')),     
    path('Education/', include('Education.urls'))
>>>>>>> Stashed changes
]
