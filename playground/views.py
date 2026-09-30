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
    difficulty = request.GET.get('difficulty', '') 
    max_time = request.GET.get('max_time', '')
    
    recipes_qs = Recipe.objects.all()
    
    # Extract unique tags for autocomplete suggestions
    unique_tags = set()
    for r in recipes_qs:
        for tag in r.get_tags_list():
            unique_tags.add(tag.lower())

    # 1. Apply Difficulty & Time Filters FIRST
    if difficulty:
        recipes_qs = recipes_qs.filter(status__iexact=difficulty)
        
    if max_time and max_time.isdigit():
        recipes_qs = recipes_qs.filter(prep_time__lte=int(max_time))

    # 2. Apply Ingredient Filter & Calculate Match Ratio
    active_ingredients = [i.strip() for i in query.split(',') if i.strip()]
    recipes_list = list(recipes_qs) # Default to all if no search query

    if active_ingredients:
        q_objects = Q()
        for ingredient in active_ingredients:
            q_objects |= Q(ingredients_list__icontains=ingredient) | Q(tags__icontains=ingredient)
        
        filtered_qs = recipes_qs.filter(q_objects).distinct()
        recipes_list = list(filtered_qs)
        
        total_searched = len(active_ingredients)
        for recipe in recipes_list:
            match_count = 0
            # Combine ingredients and tags into one lowercase string for easy checking
            recipe_text = (recipe.ingredients_list + " " + recipe.tags).lower()
            
            for ingredient in active_ingredients:
                if ingredient.lower() in recipe_text:
                    match_count += 1
            
            # Dynamically assign match data to the recipe object
            recipe.match_count = match_count
            recipe.match_total = total_searched
            match_percentage = (match_count / total_searched) * 100
            
            # Assign CSS classes based on the predefined styles in recipe_discovery.css
            if match_percentage >= 100:
                recipe.match_class = 'high'
            elif match_percentage >= 50:
                recipe.match_class = 'med'
            else:
                recipe.match_class = 'low'
        
        # Sort recipes by the highest match count descending
        recipes_list.sort(key=lambda r: r.match_count, reverse=True)

    # 3. Get User's Saved Recipes (for the bookmark icon states)
    saved_recipe_ids = []
    if request.user.is_authenticated:
        saved_recipe_ids = list(request.user.collections.values_list('recipes__id', flat=True))

    context = {
        'recipes': recipes_list,
        'active_ingredients': active_ingredients,
        'all_tags_json': json.dumps(list(unique_tags)),
        'active_difficulty': difficulty, 
        'active_time': max_time,
        'saved_recipe_ids': saved_recipe_ids,
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
    
    if collection_id:
        collection = get_object_or_404(Collection, id=collection_id, user=request.user)
        if recipe in collection.recipes.all():
            collection.recipes.remove(recipe)
            saved = False
        else:
            collection.recipes.add(recipe)
            saved = True
    else:
        # If no specific collection was passed, default to 'Favorites'
        collection, _ = Collection.objects.get_or_create(user=request.user, name="Favorites")
        if recipe in collection.recipes.all():
            collection.recipes.remove(recipe)
            saved = False
        else:
            collection.recipes.add(recipe)
            saved = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Return all user collections and which ones contain this recipe
        user_collections = list(request.user.collections.values('id', 'name'))
        recipe_collection_ids = list(recipe.collections.filter(user=request.user).values_list('id', flat=True))
        return JsonResponse({
            'saved': saved, 
            'collection': collection.name,
            'user_collections': user_collections,
            'recipe_collection_ids': recipe_collection_ids
        })
        
    return redirect(request.META.get('HTTP_REFERER', 'show_homepage'))