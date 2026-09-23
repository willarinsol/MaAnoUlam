from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.db.models import Q

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