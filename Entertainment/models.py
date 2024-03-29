from django.db import models

###################################################################################
###################################################################################

# Create your models here.

'''

'''
# define a model for categories in the QuizMe project
class Categories(models.Model):
    """Create a model for the quiz categories in QuizMe.

    :param models: models.Model
    :type models: models.TextField()
    :return: Category name and category description
    :rtype: str
    """
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
    

# define a model for subcategories in the Entertainment app
class Subcategories(models.Model):
    """Create a model for the quiz subcategories in Entertainment.

    :param models: models.Model.
    :type models: models.ForeignKey, models.TextField .
    :return: category foriegn key , subcategory and description as textfields.
    :rtype: str
    """
    # retrieve the category object representing 'Entertainment' from the Categories model
    en_category_obj = Categories.objects.get(category='Entertainment')

    # use database foreign keys to indicate relationships between categories and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    # set a default category to the primary key (pk) of the 'Entertainment' category object
    # https://docs.djangoproject.com/en/3.2/topics/db/models/#many-to-one-relationships
    # https://dnmtechs.com/setting-default-value-for-foreign-key-attribute-in-django/
    # ‘on_delete’ parameter allows one to define the behaviour when the referenced object is deleted, 
    # - providing further control over the default value
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#default
    # - according to doc, for fields like ForeignKey that map to model instances, 
    # - defaults should be the value of the field they reference (pk unless to_field is set) instead of model instances
    category = models.ForeignKey(Categories, on_delete=models.SET_DEFAULT, default=en_category_obj.pk)    

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
# create a Music class that inherits from django.db.models.Model
class Music(models.Model): 
    """Create a Music model for the subcategory in the entertainment quiz.

    :param models: models.Model.
    :type models: models.ForeignKey, models.TextField .
    :return: category foriegn key , subcategory foriegn key , question, choices and correct answer as textfields.
    :rtype: str
    """ 
    # retrieve the category object representing 'Education' from the Categories model
    en_category_obj = Categories.objects.get(category='Entertainment')
    # retrieve the subcategory object representing 'Music' from the Subcategories model
    music_subcategory_obj = Subcategories.objects.get(subcategory='Music')

    # use database foreign keys to indicate relationships between Music and categories    
    # use database foreign keys to indicate relationships between Music and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    # set a default category to the primary key (pk) of the 'en_category_obj' object
    # set the desired default subcategory to the primary key (pk) of the 'music_subcategory_obj'
    # ‘on_delete’ parameter allows one to define the behaviour when the referenced object is deleted, 
    # - providing further control over the default value
    category = models.ForeignKey(Categories, on_delete=models.SET_DEFAULT, default=en_category_obj.pk)   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, default=music_subcategory_obj.pk)       

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
        """A human-readable string representation of the Music question object in a quiz.

        :return: Return the question object
        :rtype: str
        """
        return self.question

# create a Film class that inherits from django.db.models.Model
class Film(models.Model):   
    """Create a Film model for the subcategory in the entertainment quiz.

    :param models: models.Model.
    :type models: models.ForeignKey, models.TextField .
    :return: category foriegn key , subcategory foriegn key , question, choices and correct answer as textfields.
    :rtype: str
    """ 
    # retrieve the category object representing 'Entertainment' from the Categories model
    en_category_obj = Categories.objects.get(category='Entertainment')
    # retrieve the subcategory object representing 'Film' from the Subcategories model
    film_subcategory_obj = Subcategories.objects.get(subcategory='Film')

    # use database foreign keys to indicate relationships between Film and categories    
    # use database foreign keys to indicate relationships between Film and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    # set a default category to the primary key (pk) of the 'en_category_obj' object
    # set the desired default subcategory to the primary key (pk) of the 'film_subcategory_obj'
    # ‘on_delete’ parameter allows one to define the behaviour when the referenced object is deleted, 
    # - providing further control over the default value
    category = models.ForeignKey(Categories, on_delete=models.SET_DEFAULT, default=en_category_obj.pk)   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, default=film_subcategory_obj.pk)       

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
        """A human-readable string representation of the Film question object in a quiz.

        :return: Return the question object
        :rtype: str
        """
        return self.question

class Video_Games(models.Model):
    """Create a model for the Science and nature questions in the entertainment quiz.

    :param models: models.Model.
    :type models: models.ForeignKey, models.TextField .
    :return: category foriegn key , subcategory foriegn key , question, choices and correct answer as textfields.
    :rtype: str
    """ 
    # retrieve the category object representing 'Entertainment' from the Categories model
    en_category_obj = Categories.objects.get(category='Entertainment')
    # retrieve the subcategory object representing 'Video Games' from the Subcategories model
    games_subcategory_obj = Subcategories.objects.get(subcategory='Video Games')

    # use database foreign keys to indicate relationships between Video Games and categories    
    # use database foreign keys to indicate relationships between Video Games and subcategories
    # - a ForeignKey field to show this many-to-one relationship
    # set a default category to the primary key (pk) of the 'en_category_obj' object
    # set the desired default subcategory to the primary key (pk) of the 'games_subcategory_obj'
    # ‘on_delete’ parameter allows one to define the behaviour when the referenced object is deleted, 
    # - providing further control over the default value
    category = models.ForeignKey(Categories, on_delete=models.SET_DEFAULT, default=en_category_obj.pk)   
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, default=games_subcategory_obj.pk)       
    
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
        """A human-readable string representation of the Video Games question object in a quiz.

        :return: Return the question object
        :rtype: str
        """
        return self.question    