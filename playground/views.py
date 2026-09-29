from django.shortcuts import render, get_object_or_404
from .models import Recipe, Ingredient
from django.db.models import Count, Q
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
    query = request.GET.get('ingredients', '')
    difficulty = request.GET.get('difficulty', '') # Added: Get difficulty
    max_time = request.GET.get('max_time', '')     # Added: Get max prep time

    recipes_list = Recipe.objects.all()

    # Apply Difficulty Filter (matches the 'status' field in your models.py)
    if difficulty:
        recipes_list = recipes_list.filter(status__iexact=difficulty)

    # Apply Time Filter (matches 'prep_time' in your models.py)
    if max_time and max_time.isdigit():
        recipes_list = recipes_list.filter(prep_time__lte=int(max_time))

    # Extract unique tags for the autocomplete suggestions
    unique_tags = set()
    for r in Recipe.objects.all():
        for tag in r.get_tags_list():
            unique_tags.add(tag.lower())

    # Create a list of active ingredients
    active_ingredients = [i.strip() for i in query.split(',') if i.strip()]
    if active_ingredients:
        q_objects = Q()
        for ingredient in active_ingredients:
            q_objects |= Q(ingredients_list__icontains=ingredient) | Q(tags__icontains=ingredient)
            
        recipes_list = recipes_list.filter(q_objects).distinct()

    context = {
        'recipes': recipes_list,
        'active_ingredients': active_ingredients,
        'all_tags_json': json.dumps(list(unique_tags)),
        # Pass active filters back so the template can highlight them
        'active_difficulty': difficulty, 
        'active_time': max_time,
    }
    return render(request, 'recipe_discovery.html', context)
        
    context = {
        'recipes': recipes_list,
        'active_ingredients': active_ingredients,
        'all_tags_json': json.dumps(list(unique_tags)), # 2. Pass tags to the context
    }
    return render(request, 'recipe_discovery.html', context)
