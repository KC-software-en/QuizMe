from django.db import models

###################################################################################
###################################################################################

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
Create a model for the quiz subcategories in Entertainment.
'''
# define a model for subcategories in the Entertainment app
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
    
# use Django's built-in object-relational mapping (ORM) & define the relevant classes
# -each entry in a SQL table represents a single object, this can be converted to a class instance in Python.  
# create a Music class that inherits from django.db.models.Model
class Music(models.Model):  
    '''
        Create a Music model for the subcategory in the entertainment quiz.
    '''  
    # use database foreign keys to indicate relationships between Music and categories
    # use database foreign keys to indicate relationships between Music and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE)

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
    

# create a Science_and_Nature class that inherits from django.db.models.Model
class Film(models.Model):
    '''
        Create a Science_and_Nature model for the subcategory in the entertainment quiz.
    '''
    # use database foreign keys to indicate relationships between Film and categories
    # use database foreign keys to indicate relationships between Film and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE)

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
    

class Video_Games(models.Model):
    '''
    Create a model for the Science and nature questions in the entertainment quiz.
    '''
    # use database foreign keys to indicate relationships between Video_Games and categories
    # use database foreign keys to indicate relationships between Video_Games and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE)

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