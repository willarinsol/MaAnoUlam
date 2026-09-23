from django.shortcuts import render, get_object_or_404
from .models import Recipe

def show_homepage(request):
    # Fetch the latest 4 recipes from the database
    trending_recipes = Recipe.objects.all()[:4] 
    
    # Pass them to the template
    context = {
        'recipes': trending_recipes
    }
    return render(request, 'index.html', context)

def recipe_detail(request, recipe_id):
    # Fetch the recipe by ID
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Pass it to the template
    context = {
        'recipe': recipe
    }
    return render(request, 'recipe_detail.html', context)

def recipe_discovery(request):
    recipes_list = Recipe.objects.all()  # Fetch all recipes from the database
    return render(request, 'recipe_discovery.html')