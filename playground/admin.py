from django.contrib import admin
from .models import Recipe

# This tells Django to display the Recipe model in the admin panel
admin.site.register(Recipe)