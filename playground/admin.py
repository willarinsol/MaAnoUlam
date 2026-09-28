from django.contrib import admin
from .models import Recipe, Ingredient

# This tells Django to display the Recipe model in the admin panel
admin.site.register(Recipe)
admin.site.register(Ingredient)