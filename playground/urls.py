from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.show_homepage, name='show_homepage'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('discover/', views.recipe_discovery, name='discover_recipes'),

    # Auth routes
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Collection routes
    path('saved/', views.collections_view, name='collections_view'),
    path('saved/create/', views.create_collection, name='create_collection'),
    path('saved/<int:collection_id>/rename/', views.rename_collection, name='rename_collection'),
    path('saved/<int:collection_id>/delete/', views.delete_collection, name='delete_collection'),
    path('recipe/<int:recipe_id>/toggle-save/', views.toggle_save_recipe, name='toggle_save_recipe'),
]