from django.shortcuts import render

# import HttpResponse then comment out after confirming the views rendered
# import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect

# import the Question model
from .models import Question, Choice

# the view renders an HTTP 404 error if a question with the requested ID doesn’t exist.
# import render
from django.shortcuts import get_object_or_404, render

# import reverse to generate a URL for a given view function 
# to avoid hardcoding URLs in the code, making the app more maintainable and flexible
from django.urls import reverse

#######################################################################################
#######################################################################################

# Create your views here.

'''
'''
# define index view for home page of QuizMe project referenced in Education/urls.py
def index(request): ############################################################add here
    # comment out HttpResponse once confirmed the page shows        
    # Render your template and map a URL to it
    return render(request, "index.html")

'''
'''
# create an index view that will be the home page for Education
# loads the template called edu_quiz/edu_quiz.html and passes it a context. 
# The context is a dictionary that maps template variable names to Python objects.
# comment out HttpResponse after checking it renders when running server
def index_edu(request):
    # return HttpResponse("This is the Education quiz index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, "edu_quiz/edu_quiz.html", context)

'''
'''
# write a view for the question to vote on, incl the argument question_id
# display the question text for a given quiz
# render an HTTP 404 error if a question with the requested ID doesn’t exist
# comment out HttpResponse after checking it renders when running server
def detail(request, question_id):
    # return HttpResponse(f"You're looking at question {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'edu_quiz/edu_detail.html', {'question': question})

'''
'''
# write a view for the results of the question, incl the argument question_id
# render an HTTP 404 error if a question with the requested ID doesn’t exist
# from vote(), the redirected URL will then call the 'results' view to display the final page
# comment out HttpResponse after checking it renders when running server
def results(request, question_id):
    # response = f"You're looking at the results of question {question_id}"
    # return HttpResponse(response)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'edu_quiz/edu_result.html', {'question': question})

'''
'''
# write a view to vote on a question, incl the argument question_id
# view handles the submitted data
# comment out HttpResponse after checking it renders when running server
def vote(request, question_id):
    # return HttpResponse(f"You're voting on question {question_id}") 
    # render an HTTP 404 error if a question with the requested ID doesn’t exist
    # pk refers to the primary key field of a database table
    # django automatically creates a primary key for each model
    question = get_object_or_404(Question, pk=question_id)
    
    # access submitted data by key name with a dictionary-like object- request.POST
    # use the key name choice which returns the ID of the selected choice
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice']
            )
    
    # raise a KeyError if the ID of the choice isn’t found
    # an error occurs if the mapping (dictionary) key was not located in the set of existing keys
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'edu_quiz/edu_detail.html', 
                      {'question': question,
                       'error_message': "You didn't select a choice."
                       })
    
    # else add the vote and save the choice
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # use HttpResponseRedirect instead of HttpResponse;
        # HttpResponseRedirect takes the URL to which the user will be redirected as an argument
        # return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        # use reverse function to take the name of the view and return the str value that represents the actual url
        return HttpResponseRedirect(
            reverse('Education:results', args=(question_id,))
        )




