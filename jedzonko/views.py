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
        meals = {}
        days = Dayname.objects.order_by('order')
        recipes_num = Recipe.objects.all().count()
        plans_num = Plan.objects.all().count()
        for i in range(1, 8):
            meals.update(
                {days[i - 1].name: Recipeplan.objects.filter(plan_id=last_plan.id).filter(day_name__order=i).order_by(
                    "order")})
        return render(request, "dashboard.html",
                      {"recipes_num": recipes_num, "plans_num": plans_num, "last_plan": last_plan, "meals": meals})


class SchedulesListView(View):

    def get(self, request):
        schedules = Plan.objects.all().order_by('-name')
        paginator = Paginator(schedules, 50)

        page = request.GET.get('page')
        schedules = paginator.get_page(page)
        return render(request, "app-schedules.html", {'schedules': schedules})


class RecipeAdd(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST['name']
        description = request.POST['description']
        preparation_time = request.POST['preparation_time']
        preparation_description = request.POST['preparation_description']
        ingredients = request.POST['ingredients']
        if name == '' or description == '' or preparation_time == '' or preparation_description == '' or ingredients == '' :
            komunikat = "wypełnij wszystkie pola"
            return render(request, 'app-add-schedules.html', {'komunikat': komunikat})
        recipe = Recipe.objects.create(name=name, description=description, preparation_time=preparation_time, preparation_description=preparation_description, ingredients=ingredients )
        id = recipe.id
        url = '/recipe/' + str(id) + '/'
        return redirect(url)






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


class PlanDetails(View):

    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        meals = {}
        days = Dayname.objects.order_by('order')
        for i in range(1, 8):
            meals.update(
                {days[i - 1].name: Recipeplan.objects.filter(plan_id=id).filter(day_name__order=i).order_by("order")})
        return render(request, "app-details-schedules.html", {"plan": plan, "meals": meals})

