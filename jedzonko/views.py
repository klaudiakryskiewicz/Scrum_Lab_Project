from datetime import datetime
from random import sample

from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import Recipe, Plan, Recipeplan, Dayname


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


class DashboardView(View):

    def get(self, request):
        last_plan = Plan.objects.latest("id")
        breakfasts = Recipeplan.objects.filter(plan_id=last_plan.id).filter(meal_name__icontains="breakfast").values_list("recipe__name", flat=True)
        dinners = Recipeplan.objects.filter(plan_id=last_plan.id).filter(meal_name__icontains="dinner").values_list("recipe__name", flat=True)
        suppers = Recipeplan.objects.filter(plan_id=last_plan.id).filter(meal_name__icontains="supper").values_list("recipe__name", flat=True)
        breakfasts_ids = Recipeplan.objects.filter(plan_id=last_plan.id).filter(meal_name__icontains="breakfast").values_list("recipe_id", flat=True)
        dinners_ids = Recipeplan.objects.filter(plan_id=last_plan.id).filter(meal_name__icontains="dinner").values_list("recipe_id", flat=True)
        suppers_ids = Recipeplan.objects.filter(plan_id=last_plan.id).filter(meal_name__icontains="supper").values_list("recipe_id", flat=True)
        days = Dayname.objects.all()
        recipes_num = Recipe.objects.all().count()
        return render(request, "dashboard.html", {"recipes_num": recipes_num, "last_plan": last_plan,
                                                  "days": days, "breakfasts": breakfasts,
                                                  "dinners": dinners, "suppers": suppers, "breakfasts_ids": breakfasts_ids,
                                                  "dinners_ids": dinners_ids, "suppers_ids": suppers_ids})


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
        url = '/plan/' + str(id) + '/details'
        return redirect(url)


class AddRecipeToPlan(View):

    def get(self, request):
        return render(request, "app-schedules-meal-recipe.html")
