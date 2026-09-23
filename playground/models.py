from django.db import models

# Create your models here

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField(max_length=500) 
    prep_time = models.IntegerField(help_text="Time in minutes")
    tags = models.CharField(max_length=200, help_text="e.g., Tomato, Basil") 
    
    # Text Fields
    description = models.TextField(blank=True, null=True)
    ingredients_list = models.TextField(help_text="Put each ingredient on a new line", blank=True)
    instructions = models.TextField(help_text="Put each step on a new line", blank=True)
    
    # Nutrition Fields
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0, help_text="in grams")
    carbs = models.IntegerField(default=0, help_text="in grams")
    fats = models.IntegerField(default=0, help_text="in grams")

    #difficulty 
    class Difficulty(models.TextChoices):
        EASY = 'Easy', 'Easy'
        MEDIUM = 'Medium', 'Medium'
        HARD = 'Hard', 'Hard'

    status = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY
    )
    
    def __str__(self):
        return self.title
        
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        
    def get_ingredients_list(self):
        # Splits the text box into a list wherever you hit "Enter"
        return [ing.strip() for ing in self.ingredients_list.split('\n') if ing.strip()]
        
    def get_instructions_list(self):
        return [inst.strip() for inst in self.instructions.split('\n') if inst.strip()]