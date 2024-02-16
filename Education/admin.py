# import admin to customise the admin interface, register models, and define admin views and actions
from django.contrib import admin

##############################################################################################

# import Question & Choice classes from models.py
from .models import Mythology, History

# Register your models here.
# Register the Question class, so that it will be available when we login
# to the admin page of our site.
# Register the Choice class
admin.site.register(Mythology)

# Register the Science and nature model to the admin site
admin.site.register(History)
