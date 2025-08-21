from django.shortcuts import get_object_or_404
from ninja_extra import (
    api_controller,
    route
)

from src.apps.PizzaRestaurant.models import (
    Review,
)
from src.apps.PizzaRestaurant.schemas.schemas import (
    RestaurantSchema, RestaurantOutSchema, ChefOutSchema, ChefInSchema, PizzaOutSchema, IngredientOutSchema,
    IngredientSchema, PizzaSchema, PizzaInSchema, ReviewOutSchema, ReviewInSchema, RestaurantMenuSchema,
    PizzaPatchSchema,
)
from src.apps.PizzaRestaurant.selectors import selectors
from src.apps.PizzaRestaurant.services import services


@api_controller(
    prefix_or_class='/restaurants/',
    tags=['Restaurant'],
)
class RestaurantController:
    @route.get(response=list[RestaurantOutSchema])
    def get_restaurants(self, request, ):
        return selectors.get_all_restaurants_with_chefs()

    @route.post(response=RestaurantOutSchema)
    def create_restaurant(self, request, body: RestaurantSchema):
        return services.create_restaurant(body)

    @route.put(path='{int:restaurant_id}/', response=RestaurantOutSchema)
    def update_restaurant(self, request, restaurant_id: int, body: RestaurantSchema):
        return services.update_restaurant(restaurant_id=restaurant_id, data=body)

    @route.delete(path='{int:restaurant_id}/', response={200: None}, )
    def delete_restaurant(self, request, restaurant_id: int):
        services.delete_restaurant(restaurant_id=restaurant_id)
        return 200, None

    @route.get(path='{int:restaurant_id}/menu/', response=RestaurantMenuSchema)
    def get_restaurant_menu(self, request, restaurant_id: int):
        return selectors.get_restaurant_menu(restaurant_id)


@api_controller(
    prefix_or_class='/chefs/',
    tags=['Chef'],
)
class ChefController:
    @route.get(response=list[ChefOutSchema])
    def get_chefs(self, request, ):
        return selectors.get_all_chefs_with_restaurant()

    @route.post(response=ChefOutSchema)
    def create_chef(self, request, body: ChefInSchema):
        return services.create_chef_with_restaurant(body=body)

    @route.put(path='{int:chef_id}/', response=ChefOutSchema)
    def update_chef(self, request, chef_id: int, body: ChefInSchema):
        return services.update_chef(chef_id=chef_id, body=body)

    @route.delete(path='{int:chef_id}/', response={200: None})
    def delete_chef(self, request, chef_id: int):
        services.delete_chef(chef_id=chef_id)
        return 200, None


@api_controller(
    prefix_or_class='/pizzas/',
    tags=['Pizza'],
)
class PizzaController:
    @route.get(response=list[PizzaOutSchema])
    def get_pizzas(self, request, ):
        return selectors.get_all_pizza_with_secret_ingredient_and_restaurant()

    @route.post(response=PizzaOutSchema)
    def create_pizza(self, request, body: PizzaInSchema):
        return services.create_pizza_with_restaurant_and_secret_ingredient(body)

    @route.put(path='{int:pizza_id}/', response=PizzaOutSchema)
    def update_pizza(self, request, pizza_id: int, body: PizzaSchema):
        return services.update_pizza(pizza_id=pizza_id, body=body)

    @route.patch(path='{int:pizza_id}/', response=PizzaOutSchema)
    def patch_pizza(self, request, pizza_id: int, body: PizzaPatchSchema):
        return services.update_pizza(pizza_id=pizza_id, body=body)

    @route.delete(path='{int:pizza_id}/', response={200: None})
    def delete_pizza(self, request, pizza_id: int):
        services.delete_pizza(pizza_id=pizza_id)
        return 200, None


@api_controller(
    prefix_or_class='/ingredients/',
    tags=['Ingredient'],
)
class IngredientController:
    @route.get(response=list[IngredientOutSchema])
    def get_ingredients(self, request, ):
        return selectors.get_all_ingredients()

    @route.post(response=IngredientOutSchema)
    def create_ingredient(self, request, body: IngredientSchema):
        return services.create_ingredient(body=body)


@api_controller(
    prefix_or_class='/reviews/',
    tags=['Review'],
)
class ReviewController:
    @route.get(response=list[ReviewOutSchema])
    def get_reviews(self, request, ):
        return services.get_all_reviews()

    @route.post(response=ReviewOutSchema)
    def create_review(self, request, body: ReviewInSchema):
        return services.create_review_with_restaurant(body=body)

    @route.get(path='{int:review_id}', response=ReviewOutSchema)
    def get_reviews_by_id(self, request, review_id: int):
        return get_object_or_404(Review, id=review_id)
