from django.shortcuts import get_object_or_404
from ninja_extra import (
    api_controller,
    route
)

from src.apps.PizzaRestaurant import selectors
from src.apps.PizzaRestaurant.models import (
    Restaurant,
    Chef, Pizza, Ingredient, Review,
)
from src.apps.PizzaRestaurant.schemas import (
    RestaurantSchema, RestaurantOutSchema, ChefOutSchema, ChefInSchema, PizzaOutSchema, IngredientOutSchema,
    IngredientSchema, PizzaSchema, PizzaInSchema, ReviewOutSchema, ReviewInSchema, RestaurantMenuSchema,
)
from src.apps.common.utils import update_model_instance


@api_controller(
    prefix_or_class='/restaurants/',
    tags=['Restaurant'],
)
class RestaurantController:
    @route.get(response=list[RestaurantOutSchema])
    def get_restaurants(self, request, ):
        return Restaurant.objects.select_related("chef").all()

    @route.post(response=RestaurantOutSchema)
    def create_restaurant(self, request, body: RestaurantSchema):
        return Restaurant.objects.create(**body.dict())

    @route.put(path='{int:restaurant_id}/', response=RestaurantOutSchema)
    def update_restaurant(self, request, restaurant_id: int, body: RestaurantSchema):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        update_model_instance(restaurant, body)
        return restaurant

    @route.delete(path='{int:restaurant_id}/', response={200: None}, )
    def delete_restaurant(self, request, restaurant_id: int):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        restaurant.delete()
        return 200, None

    @route.get(path='{int:restaurant_id}/menu', response=RestaurantMenuSchema)
    def get_restaurant_menu(self, request, restaurant_id: int):
        return selectors.get_restaurant_menu(restaurant_id)


@api_controller(
    prefix_or_class='/chefs/',
    tags=['Chef'],
)
class ChefController:
    @route.get(response=list[ChefOutSchema])
    def get_chefs(self, request, ):
        return Chef.objects.select_related('restaurant').all()

    @route.post(response=ChefOutSchema)
    def create_chef(self, request, body: ChefInSchema):
        chef = Chef.objects.create(
            restaurant_id=body.restaurant_id,
            **body.model_dump(exclude={"restaurant_id"})  # Pydantic v2
        )
        return chef

    @route.put(path='{int:chef_id}/', response=ChefOutSchema)
    def update_chef(self, request, chef_id: int, body: ChefInSchema):
        chef = get_object_or_404(Chef, id=chef_id)
        update_model_instance(chef, body)
        return chef

    @route.delete(path='{int:chef_id}/', response={200: None})
    def delete_chef(self, request, chef_id: int):
        chef = get_object_or_404(Chef, id=chef_id)
        chef.delete()
        return 200, None


@api_controller(
    prefix_or_class='/pizzas/',
    tags=['Pizza'],
)
class PizzaController:
    @route.get(response=list[PizzaOutSchema])
    def get_pizzas(self, request, ):
        return Pizza.objects.prefetch_related('secret_ingredient').select_related('restaurant').all()

    @route.post(response=PizzaOutSchema)
    def create_pizza(self, request, body: PizzaInSchema):
        pizza = Pizza.objects.create(
            restaurant_id=body.restaurant_id,
            **body.model_dump(exclude={"restaurant_id", "secret_ingredient"})
        )
        if body.secret_ingredient:
            pizza.secret_ingredient.set(body.secret_ingredient)

        return pizza

    @route.put(path='{int:pizza_id}/', response=PizzaOutSchema)
    def update_pizza(self, request, pizza_id: int, body: PizzaSchema):
        pizza = get_object_or_404(Pizza, id=pizza_id)
        update_model_instance(pizza, body)
        return pizza

    @route.delete(path='{int:pizza_id}/', response={200: None})
    def delete_pizza(self, request, pizza_id: int):
        pizza = get_object_or_404(Pizza, id=pizza_id)
        pizza.delete()
        return 200, None


@api_controller(
    prefix_or_class='/ingredients/',
    tags=['Ingredient'],
)
class IngredientController:
    @route.get(response=list[IngredientOutSchema])
    def get_ingredients(self, request, ):
        return Ingredient.objects.all()

    @route.post(response=IngredientOutSchema)
    def create_ingredient(self, request, body: IngredientSchema):
        return Ingredient.objects.create(**body.dict())


@api_controller(
    prefix_or_class='/reviews/',
    tags=['Review'],
)
class ReviewController:
    @route.get(response=list[ReviewOutSchema])
    def get_reviews(self, request, ):
        return Review.objects.all()

    @route.post(response=ReviewOutSchema)
    def create_review(self, request, body: ReviewInSchema):
        review = Review.objects.create(
            restaurant_id=body.restaurant_id,
            **body.model_dump(exclude={"restaurant_id"})
        )
        return review
