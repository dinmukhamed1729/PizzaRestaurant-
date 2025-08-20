from django.shortcuts import get_object_or_404

from src.apps.PizzaRestaurant.models import Restaurant


def get_restaurant_menu(restaurant_id: int):
    return get_object_or_404(Restaurant.objects
                             .prefetch_related('pizzas__secret_ingredient')
                             .select_related('chef'), id=restaurant_id)
