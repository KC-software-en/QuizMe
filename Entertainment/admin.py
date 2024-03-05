# import admin to customise the admin interface, register models, and define admin views and actions
from django.contrib import admin

##############################################################################################

# import all models.
from .models import Music, Film, Video_Games

# Register your models here.
# Register the Music model, so that it will be available on the admin site
admin.site.register(Music)

# Register the Film model, so that it will be available on the admin site
admin.site.register(Film)

# Register the Video_games model, so that it will be available on the admin site
admin.site.register(Video_Games)
