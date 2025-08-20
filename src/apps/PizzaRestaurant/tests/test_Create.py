import pytest

from src.apps.PizzaRestaurant.models import Restaurant, Ingredient, Chef, Pizza
from src.apps.PizzaRestaurant.tests.fixture import client, restaurant, ingredient
from src.apps.common.enums import Thickness
from django.test import Client


@pytest.mark.django_db(transaction=True)
def test_create_pizza_success(client, restaurant: Restaurant, ingredient: Ingredient):
    payload = {
        "name": "Маргарита",
        "cheese": "моцарелла",
        "thickness": Thickness.THIN,
        "secret_ingredient": [ingredient.id],
        "restaurant_id": restaurant.id
    }

    response = client.post("/api/pizzas/", payload, content_type="application/json")
    assert response.status_code == 200

    pizza = Pizza.objects.get(name="Маргарита")
    assert pizza.cheese == "моцарелла"
    assert pizza.thickness == Thickness.THIN
    assert ingredient in pizza.secret_ingredient.all()


@pytest.mark.django_db(transaction=True)
def test_create_pizza_invalid_thickness(client, restaurant: Restaurant, ingredient: Ingredient):
    payload = {
        "name": "Маргарита",
        "cheese": "моцарелла",
        "thickness": 'неизвестная',
        "secret_ingredient": [ingredient.id],
        "restaurant_id": restaurant.id
    }

    response = client.post("/api/pizzas/", payload, content_type="application/json")
    assert response.status_code == 400
    assert "thickness" in response.json().get("extra", {}).get("detail", [])


@pytest.mark.django_db(transaction=True)
def test_create_restaurant_success(client: Client):
    payload = {"name": "Test Restaurant", "address": "Almaty"}
    response = client.post("/api/restaurants/", payload, content_type="application/json")
    assert response.status_code == 200
    assert Restaurant.objects.filter(name="Test Restaurant", address="Almaty").exists()


@pytest.mark.django_db(transaction=True)
def test_create_restaurant_duplicate(client: Client):
    Restaurant.objects.create(name="Test Restaurant", address="Almaty")
    payload = {"name": "Test Restaurant", "address": "Almaty"}
    response = client.post("/api/restaurants/", payload, content_type="application/json")
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_create_chef_success(client: Client, restaurant: Restaurant):
    payload = {"name": "Test Chef", "restaurant_id": restaurant.id}
    response = client.post("/api/chefs/", payload, content_type="application/json")
    assert response.status_code == 200
    assert Chef.objects.filter(name="Test Chef", restaurant=restaurant).exists()


@pytest.mark.django_db(transaction=True)
def test_create_chef_invalid_restaurant(client: Client):
    payload = {"name": "Test Chef", "restaurant_id": 999}
    response = client.post("/api/chefs/", payload, content_type="application/json")
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_create_ingredient_success(client: Client):
    payload = {"name": "Test Ingredient"}
    response = client.post("/api/ingredients/", payload, content_type="application/json")
    assert response.status_code == 200
    assert Ingredient.objects.filter(name="Test Ingredient").exists()


@pytest.mark.django_db(transaction=True)
def test_create_ingredient_invalid(client: Client):
    payload = {}
    response = client.post("/api/ingredients/", payload, content_type="application/json")
    assert response.status_code == 422
