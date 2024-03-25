# import admin to customise the admin interface, register models, and define admin views and actions
from django.contrib import admin

# import all models.
from .models import Categories, Subcategories, Music, Film, Video_Games

##############################################################################################

# Register your models here.
# Register the Categories class, so that it will be available on the admin site
admin.site.register(Categories)

# Register the Subcategories class, so that it will be available on the admin site
admin.site.register(Subcategories)

# Register the Music model, so that it will be available on the admin site
admin.site.register(Music)

# Register the Film model, so that it will be available on the admin site
admin.site.register(Film)

# Register the Video_games model, so that it will be available on the admin site
admin.site.register(Video_Games)
