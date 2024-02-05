from django.db import models

###################################################################################
###################################################################################

# Create your models here.

'''
Create a model for the questions in the education quiz.
'''
# use Django's built-in object-relational mapping (ORM) & define the relevant classes
# -each entry in a SQL table represents a single object, this can be converted to a class instance in Python.  
# create a Quiz class that inherits from django.db.models.Model
class Mythology(models.Model):
    '''
    Create a model for the questions in the education quiz.
    '''
    # set variables that represent question, choices & correct_answer in the quiz
    # use TextField to store the questions
    question = models.TextField()    
    
    # use TextField to store the list of choices 
    # set default as an empty list and allow it to be blank.
    choices = models.TextField(default = list, blank = True)

    # use TextField to store the correct answer
    correct_answer = models.TextField()

    # define a __str__ method for human-readable output
    # return question
    def __str__(self):
        return self.question