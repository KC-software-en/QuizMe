from django.db import models

# Create your models here.
# use Django's built-in object-relational mapping (ORM) & define the relevant classes
# -each entry in a SQL table represents a single object, this can be converted to a class instance in Python.  
# create a question class that inherits from django.db.models.Model
class Question(models.Model):
    '''
    Create a model for the questions in the education quiz.
    '''
    # set 2 variables that represent 2 fields in the database
    # the instance of Field class CharField tells django the type of data the question holds
    # - CharField requires a max_length (used not only in the database schema but also in validation)
    # the instance of Field class DateTimeField tells django the type of data the publication date holds
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # define a __str__ method & return question_text
    def __str__(self):
        return self.question_text
    
# create a choice class that inherits from django.db.models.Model
class Choice(models.Model):
    '''
    Create a model for the choices each question has in the education quiz.
    '''
    # use database foreign keys to indicate relationships between question and choices
    # - a ForeignKey field to show this many-to-one relationship
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    
    # A Field can also have various optional arguments; in this case, set the default value of votes to 0.
    votes = models.IntegerField(default=0)

    # define a __str__ method & return choice_text
    def __str__(self):
        return self.choice_text