from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    preparation_time = models.IntegerField(default=0)
    preparation_description = models.TextField(default="")
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through="Recipeplan")

# "zastanówcie się, czy nie lepiej zamienić to na enuma w Django"
# - na razie zrobiłam dayname, jak ktoś wie co to enuma to możemy zmienić :D

class Dayname(models.Model):
    name = models.CharField(max_length=16)
    order = models.IntegerField(unique=True)


class Recipeplan(models.Model):
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(Dayname, on_delete=models.CASCADE) #nie mam pewności co do relacji tutaj




