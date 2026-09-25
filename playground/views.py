from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.db.models import Q
import json


def show_homepage(request):
    recipes = Recipe.objects.all()
    trending_recipes = recipes[:4]
    
    # Extract unique tags for the search suggestions
    unique_tags = set()
    for r in recipes:
        for tag in r.get_tags_list():
            unique_tags.add(tag.lower())
            
    context = {
        'recipes': trending_recipes,
        'all_tags_json': json.dumps(list(unique_tags)) # Pass as JSON string
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

    context = {
        'recipes': recipes_list
    }
    return render(request, 'recipe_discovery.html', context)

def recipe_discovery(request):
    query = request.GET.get('ingredients', '')
    recipes_list = Recipe.objects.all()
    
    # Create a list of active ingredients
    active_ingredients = [i.strip() for i in query.split(',') if i.strip()]

    if active_ingredients:
        from django.db.models import Q
        q_objects = Q()
        for ingredient in active_ingredients:
            q_objects |= Q(ingredients_list__icontains=ingredient) | Q(tags__icontains=ingredient)
        
        recipes_list = recipes_list.filter(q_objects).distinct()

    context = {
        'recipes': recipes_list,
        'active_ingredients': active_ingredients, # Send this to the template
    }
    return render(request, 'recipe_discovery.html', context)