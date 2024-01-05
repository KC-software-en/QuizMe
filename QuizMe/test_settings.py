# https://www.youtube.com/watch?v=41ek3VNx_6Q&t=513s
# create a test settings file in the same directory as settings.py
# instead of using postgresql, use sqlite3 database to make testing go faster from inhouse memory

# include all settings from the settings.py file located in the same directory as the module where this import statement is used
from .settings import *

# default is the alias used for the primary/default database connection
# specify the serverless database engine that Django should use for this connection
# memory specifies the name of the database
# an in-memory SQLite database should be used because are temporary & exist for the duration of the Django process. 
# They are often used for testing to create a clean slate for each test run.
DATABASES = {   
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# specify the backend used to test sending emails within your Django application
# use the in-memory email backend provided by Django (locmem ensure you don't send real emails)
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'