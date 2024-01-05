from django.shortcuts import render
# import HttpResponse 
from django.http import HttpResponse

########################################################################################
########################################################################################

# Create your views here.
# define the function index referenced in urls.py
# comment out the HttpResponse to render an html file
# render html
def index(request):
    # return HttpResponse("<h2>Hello World</h2>")
    return render(request, "index.html")

# create a function that displays an interpetation based off edu quiz choices
# pass html as parameter

