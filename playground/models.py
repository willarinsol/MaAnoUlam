from django.db import models
from django.contrib.auth.models import User
# 1. Create the new Ingredient model
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField(max_length=500)
    prep_time = models.IntegerField(help_text="Time in minutes")
    tags = models.CharField(max_length=200, help_text="e.g., Tomato, Basil")
    
    description = models.TextField(blank=True, null=True)
    # Keep this for displaying the text on the recipe detail page
    ingredients_list = models.TextField(help_text="Put each ingredient on a new line", blank=True)
    
    # 2. Add this for the search engine
    searchable_ingredients = models.ManyToManyField(Ingredient, blank=True, related_name="recipes")
    
    instructions = models.TextField(help_text="Put each step on a new line", blank=True)
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0, help_text="in grams")
    carbs = models.IntegerField(default=0, help_text="in grams")
    fats = models.IntegerField(default=0, help_text="in grams")

    servings = models.IntegerField(default=1, help_text="Number of servings")
    
    class Difficulty(models.TextChoices):
        EASY = 'Easy', 'Easy'
        MEDIUM = 'Medium', 'Medium'
        HARD = 'Hard', 'Hard'
    status = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)

    def __str__(self):
        return self.title
        
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        
    def get_ingredients_list(self):
        # Splits the text box into a list wherever you hit "Enter"
        return [ing.strip() for ing in self.ingredients_list.split('\n') if ing.strip()]
        
    def get_instructions_list(self):
        return [inst.strip() for inst in self.instructions.split('\n') if inst.strip()]


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=120)
    recipes = models.ManyToManyField('Recipe', blank=True, related_name="collections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevent duplicate collection names per user
        unique_together = ('user', 'name')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"