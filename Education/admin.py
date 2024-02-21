# import admin to customise the admin interface, register models, and define admin views and actions
from django.contrib import admin

##############################################################################################

# import Question & Choice classes from models.py
from .models import Mythology, Science_and_Nature

# Register your models here.
# Register the Mythology class, so that it will be available on the admin site
# Register the Science_and_Nature class
admin.site.register(Mythology)
admin.site.register(Science_and_Nature)

