from django.db import models

# Create your models here.
from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    # Using URLField for now to easily paste image links like in your HTML
    image_url = models.URLField(max_length=500) 
    prep_time = models.IntegerField(help_text="Time in minutes")
    
    # We'll store tags as a comma-separated string for simplicity right now
    tags = models.CharField(max_length=200, help_text="e.g., Tomato, Basil") 
    
    def __str__(self):
        return self.title
        
    def get_tags_list(self):
        # This helps us split the tags in the template
        return [tag.strip() for tag in self.tags.split(',')]