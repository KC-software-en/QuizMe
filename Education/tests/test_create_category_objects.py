
from io import StringIO
from django.core.management import call_command

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/#transactiontestcase
# import TransactionTestCase because
# tests rely on database access such as creating or querying models, 
# :. create test classes as subclasses of django.test.TestCase rather than unittest.TestCase
from django.test import TransactionTestCase

# import classes from models.py 
from ..models import Mythology

# NOTE: management commands are automatically discovered when placed within the management/commands directory of an app
# - therefore, you do not need to import create_subcategory_objects explicitly in a test case 
# - Django will find and execute the command when you call it using call_command

##############################################################################################

# https://docs.djangoproject.com/en/3.2/topics/testing/tools/#management-commands
# Management commands can be tested with the call_command() function. 
# The output can be redirected into a StringIO instance
# create a class that tests the command create_subcategory_objects
class TestCreateSubcategoryObjects(TransactionTestCase):
    def test_create_subcategory_objects(self):
        out = StringIO()
        
        # set the variables
        total_questions = 50
        category_id = 20
        model_name = Mythology
        idx = 1

        # call the command (use the name of the command which is the file name, not Command/handle)
        call_command('create_category_objects', category_id, model_name, stdout=out)
        
        # set the expected output
        progress_expected_output = f"Created quiz object {idx} out of {total_questions} for category_id:{category_id}"
        final_expected_output = f"Successfully created {total_questions} quiz objects for category_id: {category_id}"
        
        # assertions
        self.assertIn(progress_expected_output, out.getvalue(), 
                      msg='Should check that a progess message reports the creation of a specific object.')
        self.assertIn(final_expected_output, out.getvalue(), 
                      msg='Should check that a progess message reports the creation of 50 quiz objects.')