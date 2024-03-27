# create __init__.py then import this file to it

# comment out TestCase import because using unittest.
# TestCase avoids some testing complications, 
# but if tests involve the database, their behaviour may change based on the order they run. 
# This can make individual tests pass but fail when run together.
# from django.test import TestCase

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
from django.test import TransactionTestCase

# import mixer
# The Mixer is a helper to generate instances of Django or SQLAlchemy models. 
# It’s useful for testing and fixture replacement
from mixer.backend.django import mixer #

# import classes from models.py 
from ..models import Categories, Subcategories, General_Knowledge

#####################################################################################

# Create your tests here. Use `py manage.py test General_Knowledge.tests.test_models` to run tests in cmd
# after writing a test, run in cmd & it will say fail. 
# next, go to models.py and create the Question model & then it should pass
# run coverage after tests
# import classes from models.py 

'''
Create a class to test the Categories model.
'''        
# create a class to test the Categories model
# https://docs.djangoproject.com/en/3.2/topics/testing/overview/#writing-tests
class TestCategoriesModel(TransactionTestCase):
    def setUp(self):
        # no necessary conditions
        pass
    
    '''
    A function to test if the Categories model creates successfully before it coding it in models.py.
    '''
    def test_categories_model(self):        
        # create an instance of Categories model with mixer
        # textfield stores data as a str 
        category_ins = mixer.blend(Categories, category = "Category1",
                             description = "Category1 description")
        
        # assert instance was correctly created
        # incl a descriptive message with assertion
        # When the test fails, the message will be displayed along with the default error message, 
        # providing more context about what went wrong & helpful for future debugging
        self.assertIsNotNone(category_ins, msg='Should confirm question instance was created')
        # Test that obj is (or is not) an instance of cls (which can be a class or a tuple of classes, as supported by isinstance()). 
        # To check for the exact type, use assertIs(type(obj), cls). --class(cls)
        self.assertIsInstance(category_ins, Categories, msg='Should confirm that the object instantiated is from the Categories class')

        # check attributes of instance        
        expected_category = "Category1"
        expected_description = "Category1 description"        

        # assertions
        self.assertEqual(category_ins.category, expected_category,
                          msg='Should check the category attribute of the instantiated object')
        self.assertEqual(category_ins.description, expected_description, 
                             msg='Should check the description attribute of the instantiated object')        

    '''
    A function to test if the str method returns the category attribute for Categories.
    '''
    def test_return_str(self):
        # Create an instance of the Categories model with a specific question
        category_ins = Categories(category = "Category1")

        # call __str__ method
        str_outcome = str(category_ins)

        # assert that the result matches the category_ins 
        self.assertEqual(str_outcome, category_ins.category, msg='Should check that category example is in the str.')    

'''
Create a class to test the Subcategories model.
'''        
# create a class to test the Subcategories model
class TestSubcategoriesModel(TransactionTestCase):
    # setup an instance for the model used as a foreign key
    def setUp(self):
        # create an instance of Categories model with mixer
        # textfield stores data as a str 
        self.category_ins = mixer.blend(Categories, category = "Category1",
                             description = "Category1 description")
        
        # create an instance of Subcategories model with mixer
        # include the category_ins as the foreign key
        # https://stackoverflow.com/questions/44604686/how-to-test-a-model-that-has-a-foreign-key-in-django
        self.subcategory_ins = mixer.blend(Subcategories, subcategory = "Subcategory1", description = "Subcategory1 description", category = self.category_ins)
        
    '''
    A function to test if the Subcategories model creates successfully before it coding it in models.py.
    '''
    def test_subcategories_model(self): 
        # access the foreign key attribute of the subcategory_in
        subcategory_ins_fk = self.subcategory_ins.category

        # assert that the foreign key is the correct category
        self.assertEqual(subcategory_ins_fk, self.category_ins, msg='Should check that the subcategory fk is the correct category')

        # assert instance was correctly created
        # incl a descriptive message with assertion
        # When the test fails, the message will be displayed along with the default error message, 
        # providing more context about what went wrong & helpful for future debugging
        self.assertIsNotNone(self.subcategory_ins, msg='Should confirm subcategory instance was created')
        # Test that obj is (or is not) an instance of cls (which can be a class or a tuple of classes, as supported by isinstance()). 
        # To check for the exact type, use assertIs(type(obj), cls). --class(cls)
        self.assertIsInstance(self.subcategory_ins, Subcategories, msg='Should confirm that the object instantiated is from the Subcategories class')
        
        # check attributes of instance        
        expected_subcategory = "Subcategory1"
        expected_description = "Subcategory1 description"        

        # assertions
        self.assertEqual(self.subcategory_ins.subcategory, expected_subcategory,
                          msg='Should check the subcategory attribute of the instantiated object')
        self.assertEqual(self.subcategory_ins.description, expected_description, 
                             msg='Should check the description attribute of the instantiated object')        
        
    '''
    A function to test if the str method returns the subcategory attribute for Subcategories.
    '''
    def test_return_str(self):
        # call __str__ method on instance of the Subcategories model
        str_outcome = str(self.subcategory_ins)

        # assert that the result matches the subcategory_ins 
        self.assertEqual(str_outcome, self.subcategory_ins.subcategory, msg='Should check that subcategory example is in the str.')    

'''
Create a class to test the General_Knowledge model.
'''        
# create a class to test the General_Knowledge model
class TestGeneralKnowledgeModel(TransactionTestCase):
    '''
    Setup data for question model
    '''
    # setup the required data for tests
    # https://docs.djangoproject.com/en/5.0/topics/testing/overview/#writing-tests
    def setUp(self):
        # no necessary conditions
        # create an instance of Categories model with mixer
        # textfield stores data as a str 
        self.category_ins = mixer.blend(Categories, category = "Category1",
                             description = "Category1 description")
        
        # create an instance of Subcategories model with mixer
        # include the category_ins as the foreign key
        # https://stackoverflow.com/questions/44604686/how-to-test-a-model-that-has-a-foreign-key-in-django
        self.subcategory_ins = mixer.blend(Subcategories, subcategory = "Subcategory1", description = "Subcategory1 description", category = self.category_ins)
    
    '''
    A function to test if the General_Knowledge model creates successfully before it coding it in models.py.
    '''
    # create a fail test where the functions in models.py do not exist
    def test_general_knowledge_model(self):          
        # create an instance of General_Knowledge model with mixer
        # textfield stores data as a str so the list of choices will read as a str        
        quiz_ins = mixer.blend(General_Knowledge, question = "Question example",
                               choices = 'choice1, choice2, choice3, choice4',
                               correct_answer = 'choice1',
                               category = self.category_ins,
                               subcategory = self.subcategory_ins)
        
        # assert instance was correctly created
        # incl a descriptive message with assertion
        # When the test fails, the message will be displayed along with the default error message, 
        # providing more context about what went wrong & helpful for future debugging
        self.assertIsNotNone(quiz_ins, msg='Should confirm question instance was created')
        # Test that obj is (or is not) an instance of cls (which can be a class or a tuple of classes, as supported by isinstance()). 
        # To check for the exact type, use assertIs(type(obj), cls). --class(cls)
        self.assertIsInstance(quiz_ins, General_Knowledge, msg='Should confirm that the object instantiated is from the General_Knowledge class')
        
        # check attributes of instance
        # the choices are expected to be a list from the json response
        # - so use split on the choices str to return a list of substrings
        expected_question = 'Question example'
        expected_choices = ['choice1', 'choice2', 'choice3', 'choice4']
        actual_choices = quiz_ins.choices.split(', ')
        expected_correct_answer = 'choice1'

        # assertions
        self.assertEqual(quiz_ins.question, expected_question,
                          msg='Should check the question attribute of the instantiated object')
        self.assertEqual(actual_choices, expected_choices, 
                             msg='Should check the choices attribute of the instantiated object')
        self.assertEqual(quiz_ins.correct_answer, expected_correct_answer, 
                         msg='Should check the correct answer attribute of the instantiated object')        

    '''
    A function to test if the str method returns the question_text for General_Knowledge.
    '''
    def test_return_str_quiz(self):
        # Create an instance of the General_Knowledge model with a specific question
        quiz_ins = General_Knowledge(question = 'Question example')

        # call __str__ method
        str_outcome = str(quiz_ins)

        # assert that the result matches the question_ins 
        self.assertEqual(str_outcome, quiz_ins.question, msg='Question example')
    
    '''
    Create a test to check an instance of the General_Knowledge model.
    '''
    # create a test to check an instance of the General_Knowledge model
    def test_general_knowledge_instance(self):        
        # Create an instance of the General_Knowledge model with a specific question
        quiz_ins = General_Knowledge(question = 'Question example')

        # call __str__ method
        str_outcome = str(quiz_ins)

        # assert that the result matches the question_ins 
        self.assertEqual(str_outcome, quiz_ins.question, msg='Question example')   
 