from django.db import models


class Category(models.Model):
    """Категории игр"""
    name = models.CharField(max_length=50)


class Game(models.Model):
    """Игры"""
    name = models.CharField(max_length=150)
    description = models.TextField()
    release_year = models.IntegerField()
    # Картинка является ссылкой
    image = models.TextField()
    categories = models.ManyToManyField(Category, related_name="games")
