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
from venv import create
from django.test import TransactionTestCase

# import mixer
# The Mixer is a helper to generate instances of Django or SQLAlchemy models. 
# It’s useful for testing and fixture replacement
from mixer.backend.django import mixer

# import datetime for question instance
import datetime

# import classes from models.py 
from Education.models import Question, Choice 

#####################################################################################

# Create your tests here. Use `py manage.py test to run tests in cmd
# after writing a test, run in cmd & it will say fail. 
# next, go to models.py and create the Question model & then it should pass
# run coverage after tests

'''
Create a class to test the question model.
'''        
# create a class to test the question model
class TestQuestionModel(TransactionTestCase):
    '''
    Setup data for question model
    '''
    # setup the required data for tests
    # https://docs.djangoproject.com/en/5.0/topics/testing/overview/#writing-tests
    def setUp(self):
        # no necessary conditions
        pass
    
    '''
    A function to test if the question model creates successfully before it coding it in models.py.
    '''
    # create a fail test where the functions in models.py do not exist
    def test_question_model(self):        
        # create an instance of Question model with mixer
        question_ins = mixer.blend(Question, question_text = "Will this question show my educational future?",
                                pub_date = datetime.datetime.now())
        
        # assert instance was correctly created
        # incl a descriptive message with assertion
        # When the test fails, the message will be displayed along with the default error message, 
        # providing more context about what went wrong & helpful for future debugging
        self.assertIsNotNone(question_ins, 'Should confirm question instance was created')
        # Test that obj is (or is not) an instance of cls (which can be a class or a tuple of classes, as supported by isinstance()). 
        # To check for the exact type, use assertIs(type(obj), cls). --class(cls)
        self.assertIsInstance(question_ins, Question, 'Should confirm that the object instantiated is from the Question class')
        
        # check attributes of instance
        expected_question_text = 'Will this question show my educational future?'
        self.assertEqual(question_ins.question_text, expected_question_text,
                          'Should check the question_text attribute of the instantiated object')
        # assert that the pub_date attribute of the question_ins object is an instance of the datetime.datetime class
        self.assertIsInstance(question_ins.pub_date, datetime.datetime, 'Should check pub_date attribute is an instance of the datetime.datetime class')

    '''
    A function to test if the str method returns the question_text.
    '''
    def test_return_str_question(self):
        # Create an instance of the Question model with a specific question_text
        question_ins = Question(question_text = 'Select the shape within the matrix')

        # call __str__ method
        str_outcome = str(question_ins)

        # assert that the result matches the question_ins 
        self.assertEqual(str_outcome, 'Select the shape within the matrix')
    
'''
Create a class to test the choice model
'''
# create a class to test the choice model
class TestChoiceModel(TransactionTestCase):
    '''
    Setup data for choice model
    '''
    # setup the required data for tests
    # use database foreign keys to indicate relationships between question and choices
    # - a ForeignKey field to show this many-to-one relationship
    def setUp(self):        
        # use mixer to create a question instance to associate with choice instance
        self.question_ins = mixer.blend(Question, question_text = "Select the length of time you want to study")
    
    '''
    A function that tests the creation of an instance for the Choice object
    '''      
    # create a fail test for Choice
    # after writing a test, run in cmd & it will say fail. 
    # next, go to models.py and create the Question model & then it should pass
    # use mixer to create an instance of choice associated with question in setup
    def test_choice_model(self):
        choice_ins = mixer.blend(Choice, question = self.question_ins, choice_text = "Option 1", votes = 0)

        # assert instance was correctly created
        # incl a descriptive message with assertion
        self.assertIsNotNone(choice_ins, 'Should confirm choice instance was created')
        # Test that obj is (or is not) an instance of cls (which can be a class or a tuple of classes, as supported by isinstance()). 
        # To check for the exact type, use assertIs(type(obj), cls). --class(cls)
        self.assertIsInstance(choice_ins, Choice, 'Should confirm that the object instantiated is from the Choice class')

        # check attributes of choice instance  
        # assert whether the choice_text attribute of the choice_ins matches the expected value, which is 'Option 1'  
        self.assertEqual(choice_ins.choice_text, "Option 1", 'Should verify that the data saved as an attribute for choice_ins is Option 1')
        # assert whether the votes attribute of the choice_ins is equal to the expected value
        self.assertEqual(choice_ins.votes, 0, 'Should check that the votes attribute of choice_ins is the expected 0')

    '''
    A function to test if the str method returns the choice_text.
    '''
    def test_return_str_choice(self):
        # Create an instance of the Choice model with a specific choice_text
        choice_ins = Choice(choice_text = 'Pentagon')

        # call __str__ method
        str_outcome = str(choice_ins)

        # assert that the result matches the choice_ins 
        self.assertEqual(str_outcome, 'Pentagon')