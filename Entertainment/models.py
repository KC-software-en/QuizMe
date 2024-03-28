from django.db import models

###################################################################################
###################################################################################

# Create your models here.
# define a model for categories in the QuizMe project
class Categories(models.Model):
    """
    Represents a category in the system.

    Attributes:
        category (TextField): The name of the category.
        description (TextField): A description of the category.
    """

    category = models.TextField()
    description = models.TextField()
    # define a field to store the category name as text
    # define a field to store the description of the category as text
    category = models.TextField()
    description = models.TextField()

    # define a method to represent the model instance as a string
    # return the category name
    def __str__(self):
        """
        Returns the category name as a string representation of the model instance.
        """
        return self.category
    

# define a model for subcategories in the Entertainment app
class Subcategories(models.Model):
    """
    Represents subcategories within the Categories model.

    Attributes:
        category (ForeignKey): A foreign key to the Categories model representing the parent category.
            Default value is the primary key (pk) of the 'Entertainment' category object.
            Behavior on deletion of the referenced object is set to SET_DEFAULT.
            For fields like ForeignKey, defaults should be the value of the field they reference (pk).
        subcategory (TextField): The name of the subcategory as text.
        description (TextField): A description of the subcategory as text.

    Methods:
        __str__(): Returns the subcategory name as a string representation of the model instance.
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
        """
        Returns the subcategory name as a string representation of the model instance.
        """
        return self.subcategory
    

# use Django's built-in object-relational mapping (ORM) & define the relevant classes
# -each entry in a SQL table represents a single object, this can be converted to a class instance in Python.  
# create a Music class that inherits from django.db.models.Model
class Music(models.Model):   
    """
    Represents a music-related entity in the database.

    Attributes:
        category (ForeignKey): A reference to the associated category.
            Default value is the primary key of the 'en_category_obj' object.
            The 'on_delete' parameter defines behavior when the referenced object is deleted.
        subcategory (ForeignKey): A reference to the associated subcategory.
            Default value is the primary key of the 'music_subcategory_obj' object.
            'on_delete' is set to CASCADE for automatic deletion of related objects.
        question (TextField): Stores the quiz question.
        choices (TextField): Stores the list of answer choices (default is an empty list).
        correct_answer (TextField): Stores the correct answer.
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
        """
            Returns the question of the quiz.
        """
        return self.question

# create a Film class that inherits from django.db.models.Model
class Film(models.Model):        
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
        """
            Returns the question of the quiz.
        """
        return self.question
    
class Video_Games(models.Model):
    """
    Represents a film in the database.

    Attributes:
        category (ForeignKey): A foreign key relationship to the Categories model,
            representing the category of the film.
        subcategory (ForeignKey): A foreign key relationship to the Subcategories model,
            representing the subcategory of the film.
        question (TextField): Stores the film-related quiz question.
        choices (TextField): Stores the list of answer choices for the quiz.
        correct_answer (TextField): Stores the correct answer for the quiz.

    Methods:
        __str__(self):
            Returns the question of the quiz.

    Note:
        - The `on_delete` parameter specifies the behavior when the referenced object is deleted.
          In this case, we use `models.SET_DEFAULT` to set the default value.
        - The default category and subcategory are set to the primary keys (pks) of the respective objects.
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
        """
            Returns the question of the quiz.
        """
        return self.question    