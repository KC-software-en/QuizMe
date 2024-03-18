from django.db import models

############################################################################################

# Create your models here.

'''
Create a model for the quiz categories in QuizMe.
'''
# define a model for categories in the QuizMe project
class Categories(models.Model):
    # define a field to store the category name as text
    # define a field to store the description of the category as text
    category = models.TextField()
    description = models.TextField()

    # define a method to represent the model instance as a string
    # return the category name
    def __str__(self):
        return self.category
    
'''
Create a model for the quiz subcategories in General_Knowledge.
'''
# define a model for subcategories in the General_Knowledge app
class Subcategories(models.Model):
    # use database foreign keys to indicate relationships between categories and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)   

    # define a field to store the subcategory name as text
    subcategory = models.TextField()

    # define a field to store the description of the subcategory as text
    description = models.TextField()

    # define a method to represent the model instance as a string
    # return the subcategory name 
    def __str__(self):
        return self.subcategory
    

'''
Create a General Knowledge model for the quiz.
'''
# use Django's built-in object-relational mapping (ORM) & define the relevant classes
# -each entry in a SQL table represents a single object, this can be converted to a class instance in Python.  
# create a General Knowledge class that inherits from django.db.models.Model
class General_Knowledge(models.Model):   
    # use database foreign keys to indicate relationships between General_Knowledge and categories    
    # - a ForeignKey field to show this many-to-one relationship
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)       

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
    