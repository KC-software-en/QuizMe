# import admin to customise the admin interface, register models, and define admin views and actions
from django.contrib import admin

# import classes from models.py
from .models import Categories, Subcategories, Mythology, History, Science_and_Nature

##############################################################################################

# Register your models here.

# Register the Categories class, so that it will be available on the admin site
admin.site.register(Categories)

# Register the Subcategories class, so that it will be available on the admin site
admin.site.register(Subcategories)

# Register the Mythology class, so that it will be available on the admin site
admin.site.register(Mythology)

# Register the History model to the admin site
admin.site.register(History)

# Register the Science and nature model to the admin site
admin.site.register(Science_and_Nature)
