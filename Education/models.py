# import models
from django.db import models

###################################################################################
###################################################################################

# Create your models here.

# define a model for categories in the QuizMe project
class Categories(models.Model):
    # define a field to store the category name as text
    # define a field to store the description of the category as text
    category = models.TextField()
    description = models.TextField()

    # define a method to represent the model instance as a string
    # return the category name
    def __str__(self):
        """A human-readable string representation of the category object.

        :return: Return the category object
        :rtype: str
        """
        return self.category
        
# define a model for the quiz subcategories in the Education app
class Subcategories(models.Model):
    # use database foreign keys to indicate relationships between categories and subcategories
    # - a ForeignKey field to show this many-to-one relationship ¹
    # set a default category to the primary key (pk) of the 'Education' category object²
    # https://docs.djangoproject.com/en/3.2/topics/db/models/#many-to-one-relationships
    # https://dnmtechs.com/setting-default-value-for-foreign-key-attribute-in-django/
    # ‘on_delete’ parameter allows one to define the behaviour when the referenced object is deleted, 
    # - providing further control over the default value
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#default
    # - according to doc, for fields like ForeignKey that map to model instances, 
    # - defaults should be the value of the field they reference (pk unless to_field is set) instead of model instances³
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default='Education')

    # define a field to store the subcategory name as text
    subcategory = models.TextField()

    # define a field to store the description of the subcategory as text
    description = models.TextField()

    # define a method to represent the model instance as a string
    # return the subcategory name 
    def __str__(self):
        """A human-readable string representation of the subcategory object.

        :return: Return the subcategory object
        :rtype: str
        """
        return self.subcategory

# use Django's built-in object-relational mapping (ORM) & define the relevant classes
# -each entry in a SQL table represents a single object, this can be converted to a class instance in Python.  
# create a Mythology class that inherits from django.db.models.Model
class Mythology(models.Model):          
    # use database foreign keys to indicate relationships between Mythology and categories    
    # use database foreign keys to indicate relationships between Mythology and subcategories
    # - a ForeignKey field to show this many-to-one relationship    
    # ‘on_delete’ parameter allows one to define the behaviour when the referenced object is deleted, 
    # - with cascade all related objects will also be deleted. This is useful for maintaining referential integrity in the database
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default='Education')   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, default='Mythology')   

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
        """A human-readable string representation of the Mythology question object.

        :return: Return the question object
        :rtype: str
        """
        return self.question

# create a Science_and_Nature class that inherits from django.db.models.Model
class Science_and_Nature(models.Model):        
    # use database foreign keys to indicate relationships between Education and categories    
    # use database foreign keys to indicate relationships between Science_and_Nature and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    # set the category default value to Education 
    # set the subcategory default value to Science_and_Nature
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default='Education')   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, default='Science_and_Nature')   

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
        """A human-readable string representation of the Science & Nature question object.

        :return: Return the question object
        :rtype: str
        """
        return self.question
    
# create a History class that inherits from django.db.models.Model
class History(models.Model):      
    # use database foreign keys to indicate relationships between History and categories
    # call the function to retrieve the desired default category
    # use database foreign keys to indicate relationships between History and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    # set the category default value to Education
    # set the subcategory default value to History
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default='Education')   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, default='History')   

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
        """A human-readable string representation of the History question object.

        :return: Return the question object
        :rtype: str
        """
        return self.question    
    
