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

# import requests to use the API for edu quiz
import requests

# import html to handle potential HTML entities and aid rendering
import html

# import random to shuffle choices rendered in the form
import random

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
Create a view for the home page of education quizzes.
'''
# display the category of the education quiz
# https://www.youtube.com/watch?v=sgEhb50YSTE
# get json reponse for trivia categories from open trivia db
# index category from the dictionary id
def index_edu(request, category_id=20):
    # get Category Lookup url
    category_lookup = 'https://opentdb.com/api_category.php'
    # store url in a variable as a json response
    response = requests.get(category_lookup).json()

    # write Categories to a json file
    # use an indent to ensure each category prints on separate lines
    with open("quiz_categories.json", "w") as f:
    json.dump(response, f, indent=4)
    
    # get the trivia categories values from dictionary provided in json response
    # place an empty list as the default argument if the key is not found - should avoid errors in subsequent code
    trivia_categories = response.get("trivia_categories", [])

    # initialise a variable for the chosen category from the json response
    selected_category = None
    category_name = None

    # iterate over trivia categories to find the category id specified in the function as a parameter
    for category in trivia_categories:
        # cast category_id to int for error handling
        if category.get("id") == int(category_id):
            # assign the current category to the selected_category variable
            selected_category = category
            # exit the loop when the desired category is found
            break
            
        # get the name of the category if the id exists for the selected category
        if selected_category:
            category_name = selected_category.get("name")

    # the response is the dictionary for trivia categories
    # pass all the context variables into a single dictionary to render in the template correctly
    return render(request, 'edu_quiz/edu_quiz.html', {'selected_category':selected_category, 'category_name': category_name}) 

'''
'''
# create a function to generate a selection of questions
# include parameters (expected variables) for the number of questions you want & the category for them
# create a varible to store the API url for the myth quizzes
# use an f-str to pass in the parameter for quantity
# -> place {} around 50 in the url then replace '50' with 'quantity'
# then place {} around the category id (from quiz_cat.json)for myth & replace '20' with 'category'
# return a list
def get_questions(quantity: int, category: int):
    mythology_url = f"https://opentdb.com/api.php?amount=50&category=20"
    response = requests.get(mythology_url)
    # get a json response or else the above will only give a status code
    json_response = response.json()
    # save json response as a variable to pass into template
    questions = json_response["results"]
    # return the list of dictionaries in the json response which contains the questions/answers
    # note the json response is a dictionary where its :value ("results") contains a list of dictionaries    
    #return json_response["results"]##
    return render(request, 'edu_quiz/edu_detail.html', {'questions': questions})

# rearrange the options of answers
# use the random module & its shuffle function to rearrange
# return a list of choices
def mix_choices(choices: list):
    random.shuffle(choices)
    #return choices##
    return render(request, 'edu_quiz/edu_detail.html', {'choices': choices})

# display the choices in detail view
# iterate over choices with for loop
def get_choices():
    questions = get_questions(50, 20)
    for question in questions:
        question = question["question"]
        correct_answer = json_response["results"]["correct_answer"]


#def detail(choices: list):
    #return render(request, 'edu_quiz/edu_detail.html', {'question': question})

# save the selected choice in votes view

# display quiz result in results view
# calculate the score and pass it to the template. 
# use the request.POST dictionary to access the user’s answers and compare them with the correct answers
def results():
    if request.method == "POST":
        result = 0
        for question in questions:
            if request.POST[question["question"]] == question["correct_answer"]:
                result += 1
        return render(request, 'edu_quiz/edu_result.html', {'questions': questions, "result": result})       



#####################################previous work##############################################
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

'''
To use the Open Trivia Database API generated URL in a Django project, you need to do the following steps:

Import the requests module to make HTTP requests to the API.
Use the requests.get() function to send a GET request to the API URL and store the response object.
Use the response.json() method to parse the response data as a JSON object.
Access the results key of the JSON object to get a list of trivia questions and their attributes.
Loop through the list and display the questions and answer choices in your Django template using the {{ variable }} syntax.
Optionally, you can use the session_token parameter to avoid getting repeated questions from the API.
Here is an example of how to use the Open Trivia Database API generated URL in a Django project:

# views.py
import requests
from django.shortcuts import render

def trivia(request):
    # Generate the API URL with your desired parameters
    api_url = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=multiple"
    # Send a GET request to the API and store the response object
    response = requests.get(api_url)
    # Parse the response data as a JSON object
    data = response.json()
    # Access the results key to get a list of trivia questions
    questions = data["results"]
    # Render the trivia template with the questions as context
    return render(request, "trivia.html", {"questions": questions})

<!-- trivia.html -->
<h1>Trivia Time</h1>
{% for question in questions %}
    <div class="question">
        <p>{{ question.question }}</p>
        <ul>
            <li>{{ question.correct_answer }}</li>
            {% for answer in question.incorrect_answers %}
                <li>{{ answer }}</li>
            {% endfor %}
        </ul>
    </div>
{% endfor %}
'''


