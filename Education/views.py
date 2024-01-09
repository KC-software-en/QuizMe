from django.shortcuts import render

# import HttpResponse then comment out after confirming the views rendered
# import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect

# import the Question model
from .models import Question, Choice

# the view renders an HTTP 404 error if a question with the requested ID doesn’t exist.
# import render
from django.shortcuts import get_object_or_404, render

#
from django.urls import reverse

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

# comment out HttpResponse after checking it renders when running server
def results(request, question_id):
    # response = f"You're looking at the results of question {question_id}"
    # return HttpResponse(response)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'edu_quiz/edu_result.html', {'question': question})

# 
# comment out HttpResponse after checking it renders when running server
def vote(request, question_id):
    # return HttpResponse(f"You're voting on question {question_id}") 
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice']
            )
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'edu_quiz/edu_detail.html', 
                      {'question': question,
                       'error_message': "You didn't select a choice."
                       })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully
        # dealing with POST data. This prevents data from being
        # posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('Education:results', args=(question_id,))
        )




