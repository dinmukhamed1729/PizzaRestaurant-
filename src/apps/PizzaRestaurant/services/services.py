from urllib.request import Request

from django.shortcuts import get_object_or_404
from ninja import Schema

from src.apps.PizzaRestaurant.models import Restaurant, Chef, Pizza, Ingredient, Review
from src.apps.common.utils import update_model_instance


def create_restaurant(body: Schema):
    return Restaurant.objects.create(**body.dict())


def update_restaurant(restaurant_id: int, data: Schema):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    update_model_instance(restaurant, data)
    return restaurant


def delete_restaurant(restaurant_id: int):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()


def create_chef_with_restaurant(body: Schema):
    return Chef.objects.create(
        restaurant_id=body.restaurant_id,
        **body.model_dump(exclude={"restaurant_id"})
    )


def update_chef(chef_id: int, body: Schema):
    chef = get_object_or_404(Chef, id=chef_id)
    update_model_instance(chef, body)
    return chef


def delete_chef(chef_id: int):
    chef = get_object_or_404(Chef, id=chef_id)
    chef.delete()


def create_pizza_with_restaurant_and_secret_ingredient(body: Schema):
    pizza = Pizza.objects.create(
        restaurant_id=body.restaurant_id,
        **body.model_dump(exclude={"restaurant_id", "secret_ingredient"})
    )
    if body.secret_ingredient:
        pizza.secret_ingredient.set(body.secret_ingredient)

    return pizza


def update_pizza(pizza_id: int, body: Schema):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    update_model_instance(pizza, body)
    return pizza


def delete_pizza(pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    pizza.delete()


def create_ingredient(body: Schema):
    return Ingredient.objects.create(**body.dict())


def get_all_reviews():
    return Review.objects.all()


def create_review_with_restaurant(body: Schema):
    review = Review.objects.create(
            restaurant_id=body.restaurant_id,
            **body.model_dump(exclude={"restaurant_id"})
        )
    return review