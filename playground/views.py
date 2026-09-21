from django.shortcuts import render
from .models import Recipe

def show_homepage(request):
    # Fetch the latest 4 recipes from the database
    trending_recipes = Recipe.objects.all()[:4] 
    
    # Pass them to the template
    context = {
        'recipes': trending_recipes
    }
    return render(request, 'index.html', context)