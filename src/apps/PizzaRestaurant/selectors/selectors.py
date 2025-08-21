from django.shortcuts import get_object_or_404

from src.apps.PizzaRestaurant.models import Restaurant, Chef, Pizza, Ingredient


def get_restaurant_menu(restaurant_id: int):
    return get_object_or_404(Restaurant.objects
                             .prefetch_related('pizzas__secret_ingredient')
                             .select_related('chef'), id=restaurant_id)


def get_all_restaurants_with_chefs():
    return Restaurant.objects.select_related("chef").all()


def get_all_chefs_with_restaurant():
    return Chef.objects.select_related('restaurant').all()


def get_all_pizza_with_secret_ingredient_and_restaurant():
    return Pizza.objects.prefetch_related('secret_ingredient').select_related('restaurant').all()


def get_all_ingredients():
    return Ingredient.objects.all()