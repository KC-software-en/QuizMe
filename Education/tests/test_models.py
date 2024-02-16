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
from mixer.backend.django import mixer

# import classes from models.py 
from ..models import Mythology


#####################################################################################

# Create your tests here. Use `py manage.py test Education.tests.test_models` to run tests in cmd
# after writing a test, run in cmd & it will say fail. 
# next, go to models.py and create the Question model & then it should pass
# run coverage after tests

'''
Create a class to test the Mythology model.
'''        
# create a class to test the Mythology model
class TestMythologyModel(TransactionTestCase):
    '''
    Setup data for question model
    '''
    # setup the required data for tests
    # https://docs.djangoproject.com/en/5.0/topics/testing/overview/#writing-tests
    def setUp(self):
        # no necessary conditions
        pass
    
    '''
    A function to test if the Mythology model creates successfully before it coding it in models.py.
    '''
    # create a fail test where the functions in models.py do not exist
    def test_mythology_model(self):        
        # create an instance of Mythology model with mixer
        # textfield stores data as a str so the list of choices will read as a str
        quiz_ins = mixer.blend(Mythology, question = "Question example",
                             choices = 'choice1, choice2, choice3, choice4',
                               correct_answer = 'choice1')
        
        # assert instance was correctly created
        # incl a descriptive message with assertion
        # When the test fails, the message will be displayed along with the default error message, 
        # providing more context about what went wrong & helpful for future debugging
        self.assertIsNotNone(quiz_ins, msg='Should confirm question instance was created')
        # Test that obj is (or is not) an instance of cls (which can be a class or a tuple of classes, as supported by isinstance()). 
        # To check for the exact type, use assertIs(type(obj), cls). --class(cls)
        self.assertIsInstance(quiz_ins, Mythology, msg='Should confirm that the object instantiated is from the Mythology class')
        
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
    A function to test if the str method returns the question_text.
    '''
    def test_return_str_quiz(self):
        # Create an instance of the Mythology model with a specific question
        quiz_ins = Mythology(question = 'Question example')

        # call __str__ method
        str_outcome = str(quiz_ins)

        # assert that the result matches the question_ins 
        self.assertEqual(str_outcome, quiz_ins.question, msg='Question example')
    
    '''
    Create a test to check an instance of the Mythology model.
    '''
    # create a test to check an instance of the Mythology model
    def test_mythology_instance(self):
        # use mixer to create an instance of the Mythology model
        quiz_instance = mixer.blend(Mythology)

        # assert that the instance was successful
        self.assertIsInstance(quiz_instance, Mythology, msg='Should confirm that the object instantiated is from the Mythology class')
    
    
    