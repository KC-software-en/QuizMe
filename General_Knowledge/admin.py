# import admin to customise the admin interface, register models, and define admin views and actions
from django.contrib import admin

# import classes from models.py
from .models import Categories, Subcategories, General_Knowledge

##############################################################################################

# Register your models here.
# Register the Categories class, so that it will be available on the admin site
admin.site.register(Categories)

# Register the Subcategories class, so that it will be available on the admin site
admin.site.register(Subcategories)

# Register the General_Knowledge model to the admin site
admin.site.register(General_Knowledge)