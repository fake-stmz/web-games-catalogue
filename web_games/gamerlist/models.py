from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
class Game(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    release_year = models.IntegerField()
    image = models.TextField()
    categories = models.ManyToManyField(Category, related_name="games")
