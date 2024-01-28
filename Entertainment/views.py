from django.shortcuts import render

def entertainment_page(request):
    # Quiz page
    return render(request('quiz_page.html'))
   

