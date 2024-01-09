from django.shortcuts import render

# import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect

# import the Question model
from .models import Question

# the view renders an HTTP 404 error if a question with the requested ID doesn’t exist.
from django.shortcuts import get_object_or_404

#######################################################################################
#######################################################################################

# Create your views here.

# create an index view that will be the home page for the project
# loads the template called polls/poll.html and passes it a context. 
# The context is a dictionary that maps template variable names to Python objects.
# comment out HttpResponse after checking it renders when running server
def index_edu(request):
    # return HttpResponse("This is the Education quiz index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, "edu_quiz/edu_quiz.html", context)

# display the question text for a given quiz
# comment out HttpResponse after checking it renders when running server
def detail(request, question_id):
    # return HttpResponse(f"You're looking at question {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'edu_quiz/edu_detail.html', {'question': question})


def results(request, question_id):
    response = f"You're looking at the results of question {question_id}"
    return HttpResponse(response)

def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}") 
