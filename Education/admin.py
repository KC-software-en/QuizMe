# import admin to customise the admin interface, register models, and define admin views and actions
from django.contrib import admin

##############################################################################################

# import Question & Choice classes from models.py
from .models import Quiz

# Register your models here.
# Register the Question class, so that it will be available when we login
# to the admin page of our site.
# Register the Choice class
admin.site.register(Quiz)
