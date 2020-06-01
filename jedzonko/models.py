from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=48)
    ingredients = models.CharField(max_length=48)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)
