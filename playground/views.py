import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Recipe, Ingredient, Collection

# ==========================================
# 1. ORIGINAL CORE VIEWS
# ==========================================

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

def about_view(request):
    return render(request, 'about.html')

def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

def recipe_discovery(request):
    query = request.GET.get('ingredients', '')
    difficulty = request.GET.get('difficulty', '') # Added: Get difficulty
    max_time = request.GET.get('max_time', '')     # Added: Get max prep time

    recipes_list = Recipe.objects.all()
    
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
        'all_tags_json': json.dumps(list(unique_tags)),
    }
    return render(request, 'recipe_discovery.html', context)


# ==========================================
# 2. AUTHENTICATION VIEWS
# ==========================================

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create a starter collection for new users
            Collection.objects.create(user=user, name="Favorites")
            login(request, user)
            return redirect('show_homepage')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next') or 'show_homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('show_homepage')


# ==========================================
# 3. COLLECTION & SAVED RECIPE VIEWS
# ==========================================

@login_required
def collections_view(request):
    collections = request.user.collections.prefetch_related('recipes').all()
    return render(request, 'saved_recipes.html', {'collections': collections})

@login_required
@require_POST
def create_collection(request):
    name = request.POST.get('name', '').strip()
    if name:
        Collection.objects.get_or_create(user=request.user, name=name)
    return redirect('collections_view')

@login_required
@require_POST
def rename_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, user=request.user)
    new_name = request.POST.get('new_name', '').strip()
    if new_name:
        collection.name = new_name
        collection.save()
    return redirect('collections_view')

@login_required
@require_POST
def delete_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, user=request.user)
    collection.delete()
    return redirect('collections_view')

@login_required
@require_POST
def toggle_save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    collection_id = request.POST.get('collection_id')

    # Default to user's first collection if none specified
    if collection_id:
        collection = get_object_or_404(Collection, id=collection_id, user=request.user)
    else:
        collection, _ = Collection.objects.get_or_create(user=request.user, name="Favorites")

    if recipe in collection.recipes.all():
        collection.recipes.remove(recipe)
        saved = False
    else:
        collection.recipes.add(recipe)
        saved = True

    # Support JSON requests from bookmark icons, fallback to redirect
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'saved': saved, 'collection': collection.name})
    return redirect(request.META.get('HTTP_REFERER', 'show_homepage'))