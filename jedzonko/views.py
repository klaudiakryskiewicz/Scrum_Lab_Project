from datetime import datetime
from random import sample

from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        recipes = Recipe.objects.order_by('?')[:3]
        # jak nie zrobię tego fora to pokazuje mi losową nazwę, losowe składniki i losowy opis XD
        for recipe in recipes:
            print(recipe.name, recipe.ingredients, recipe.description)
        return render(request, "index.html", {'recipes': recipes, "actual_date": datetime.now()})


class RecipeList(View):

    def get(self, request):
        return render(request, "app-recipes.html")
