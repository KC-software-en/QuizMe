
from io import StringIO
import sys
from django.core.management import call_command

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
from django.test import TransactionTestCase

# import classes from models.py 
from ..models import Mythology

#  import unittest to write tests that are not necessarily tied to Django and can be used in any Python project e.g. get API response from open trivia db
from unittest.mock import patch, MagicMock, Mock

# NOTE: management commands are automatically discovered when placed within the management/commands directory of an app
# - therefore, you do not need to import create_subcategory_objects explicitly in a test case 
# - Django will find and execute the command when you call it using call_command

##############################################################################################

# Create your tests here. Use `py manage.py test Education.tests.test_create_category_objects` to run tests in cmd
# after writing a test, run in cmd & it will say fail. 
# next, go to create_category_objects.py and create the command. Then it should pass
# run coverage after tests
'''
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#management-commands
# Management commands can be tested with the call_command() function. 
# The output can be redirected into a StringIO instance
# create a class that tests the command create_subcategory_objects
class TestCreateSubcategoryObjects(TransactionTestCase):
    @patch('Education.utils.requests.get')
    def test_create_subcategory_objects(self, mock_get_request):
        mock_ok_response = MagicMock()
        mock_ok_response.status_code = 200
        mock_ok_response.json.return_value = {
            "results":[
                {"type":"type1",
                 "difficulty":"level",
                 "category":"category1",
                 "question":"question1",
                 "correct_answer":"correct_answer1",
                 "incorrect_answers":[
                     "incorrect_answer",
                     "incorrect_answer2",
                     "incorrect_answer3",                     
                 ]
                 }
            ]
        }

        # set the return value for response of mock_get as mock_response
        mock_get_request.return_value = mock_ok_response

        out = StringIO() 
        ##sys.stdout = out       
        
        # set the variables
        total_questions = 50
        category_id = 20
        category_name = 'Mythology'
        idx = 1

        # call the command (use the name of the command which is the file name, not Command/handle)
        call_command('create_category_objects', category_id, category_name, stdout=out)
        print(f"out:{out.getvalue()}")##

        # set the expected output
        progress_expected_output = f"Created quiz object {idx} out of {total_questions} for category_id:{category_id}"
        final_expected_output = f"Successfully created {total_questions} quiz objects for category_id: {category_id}"
        
        ##sys.stdout = sys.__stdout__

        # assertions
        self.assertIn(progress_expected_output, out.getvalue(), 
                      msg='Should check that a progess message reports the creation of a specific object.')
        self.assertIn(final_expected_output, out.getvalue(), 
                      msg='Should check that a progess message reports the creation of 50 quiz objects.')
'''
class TestCreateSubcategoryObjects2(TransactionTestCase):
    def test_create_subcategory_objects2(self):
        out = StringIO
        call_command('create_category_objects', 20, 'Mythology', stdout=out)
        self.assertIn('Created quiz object', out.getvalue())
        self.assertIn('Successfully created', out.getvalue())
