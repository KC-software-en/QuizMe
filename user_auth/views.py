from django.shortcuts import render

# Create your views here.
def user_login(request):
    return render(request, 'login.html')

def user_logout(request):
    return render(request, 'logout.html')

def user_register(request):
    return render(request, 'register.html')
    