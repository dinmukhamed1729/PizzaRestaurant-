from django.db import IntegrityError
from django.http import JsonResponse
from ninja_extra import NinjaExtraAPI

from src.apps.PizzaRestaurant.api.views import (
    RestaurantController,
    ChefController,
    PizzaController,
    IngredientController,
    ReviewController,
)

api_restaurant = NinjaExtraAPI(
    title='Restaurant API',
)
controllers = [
    RestaurantController,
    ChefController,
    PizzaController,
    IngredientController,
    ReviewController,
]

api_restaurant.register_controllers(*controllers)


@api_restaurant.exception_handler(IntegrityError)
def handle_integrity_error(request, exc: IntegrityError):
    detail = str(exc)
    return JsonResponse(
        {"message": "Bad Request", "extra": {"detail": detail}},
        status=400
    )
