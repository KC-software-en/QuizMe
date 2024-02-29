# import admin to customise the admin interface, register models, and define admin views and actions
from django.contrib import admin

# import classes from models.py
from .models import General_Knowledge

##############################################################################################

# Register your models here.
# Register the General_Knowledge model to the admin site
admin.site.register(General_Knowledge)