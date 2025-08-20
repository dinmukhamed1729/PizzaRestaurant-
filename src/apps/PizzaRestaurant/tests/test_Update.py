import pytest
from django.test import Client

from src.apps.PizzaRestaurant.models import Pizza, Ingredient, Restaurant, Chef
from src.apps.PizzaRestaurant.tests.fixture import client, restaurant, chef, pizza, ingredient
from src.apps.common.enums import Thickness


@pytest.mark.django_db(transaction=True)
def test_update_pizza(client: Client, pizza: Pizza, ingredient: Ingredient):
    url = f"/api/pizzas/{pizza.id}/"
    payload = {
        "name": "Пепперони",
        "cheese": "чеддер",
        "thickness": Thickness.CLASSIC,
        "secret_ingredient": [ingredient.id],
    }
    response = client.put(url, payload, content_type="application/json")
    assert response.status_code == 200

    pizza.refresh_from_db()
    assert pizza.name == "Пепперони"
    assert pizza.cheese == "чеддер"
    assert pizza.thickness == Thickness.CLASSIC
    assert ingredient in pizza.secret_ingredient.all()


@pytest.mark.django_db(transaction=True)
def test_update_chef(client: Client, chef: Chef, restaurant: Restaurant):
    url = f"/api/chefs/{chef.id}/"
    payload = {
        "name": "Гордон Рамзи",
        "restaurant_id": restaurant.id
    }
    response = client.put(url, payload, content_type="application/json")
    assert response.status_code == 200

    chef.refresh_from_db()
    assert chef.name == "Гордон Рамзи"
    assert chef.restaurant.id == restaurant.id


@pytest.mark.django_db(transaction=True)
def test_update_restaurant(client: Client, restaurant: Restaurant):
    url = f"/api/restaurants/{restaurant.id}/"
    payload = {
        "name": "Итальянский ресторан",
        "address": "Нур-Султан"
    }
    response = client.put(url, payload, content_type="application/json")
    assert response.status_code == 200

    restaurant.refresh_from_db()
    assert restaurant.name == "Итальянский ресторан"
    assert restaurant.address == "Нур-Султан"
