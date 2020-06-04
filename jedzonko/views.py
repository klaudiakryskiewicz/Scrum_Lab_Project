from datetime import datetime
from random import sample

from django.core.paginator import Paginator
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
        recipes = Recipe.objects.order_by('-votes', '-created')
        paginator = Paginator(recipes, 50)

        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {'recipes': recipes})


class DashboardView(View):

    def get(self, request):
        last_plan = Plan.objects.latest("id")
        mon_meals = Recipeplan.objects.filter(plan_id=last_plan.id).filter(day_name__order=1).order_by("order")
        tue_meals = Recipeplan.objects.filter(plan_id=last_plan.id).filter(day_name__order=2).order_by("order")
        wed_meals = Recipeplan.objects.filter(plan_id=last_plan.id).filter(day_name__order=3).order_by("order")
        thu_meals = Recipeplan.objects.filter(plan_id=last_plan.id).filter(day_name__order=4).order_by("order")
        fri_meals = Recipeplan.objects.filter(plan_id=last_plan.id).filter(day_name__order=5).order_by("order")
        sat_meals = Recipeplan.objects.filter(plan_id=last_plan.id).filter(day_name__order=6).order_by("order")
        sun_meals = Recipeplan.objects.filter(plan_id=last_plan.id).filter(day_name__order=7).order_by("order")
        days = Dayname.objects.all().order_by("id")
        recipes_num = Recipe.objects.all().count()
        return render(request, "dashboard.html", {"recipes_num": recipes_num, "last_plan": last_plan,
                                                  "days": days, "mon_meals": mon_meals, "tue_meals": tue_meals,
                                                  "wed_meals": wed_meals, "thu_meals": thu_meals,
                                                  "fri_meals": fri_meals,
                                                  "sat_meals": sat_meals, "sun_meals": sun_meals, })


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

    def post(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        if request.POST['submit'] == 'Polub przepis':
            recipe.votes += 1
        elif request.POST['submit'] == 'Nie lubię tego przepisu':
            recipe.votes -= 1
        recipe.save()
        url = "/recipe/" + str(id) + "/"
        return redirect(url)
