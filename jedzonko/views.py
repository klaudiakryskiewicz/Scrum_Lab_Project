from datetime import datetime
from random import sample

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import Recipe, Plan


class IndexView(View):

    def get(self, request):
        recipes = Recipe.objects.order_by('?')[:3]
        # jak nie zrobię tego fora to pokazuje mi losową nazwę, losowe składniki i losowy opis XD
        for recipe in recipes:
            print(recipe.name, recipe.ingredients, recipe.description)
        return render(request, "index.html", {'recipes': recipes, "actual_date": datetime.now()})


class RecipeList(View):

    def get(self, request):
        recipes = Recipe.objects.order_by('-votes', '-created')
        paginator = Paginator(recipes, 50)

        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {'recipes': recipes})


class DashboardView(View):

    def get(self, request):
        recipes_num = Recipe.objects.all().count()
        return render(request, "dashboard.html", {"recipes_num": recipes_num})


class PlansList(View):

    def get(self, request):
        return render(request, "app-schedules.html")


class RecipeAdd(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")


class AddPlan(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST['name']
        description = request.POST['description']
        if name == '' or description == '':
            komunikat = "wypełnij wszystkie pola"
            return render(request, 'app-add-schedules.html', {'komunikat': komunikat})
        plan = Plan.objects.create(name=name, description=description)
        id = plan.id
        url = '/plan/' + str(id) + '/'
        return redirect(url)


class AddRecipeToPlan(View):

    def get(self, request):
        return render(request, "app-schedules-meal-recipe.html")


class RecipeDetails(View):

    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        return render(request, "app-recipe-details.html", {"recipe": recipe})
