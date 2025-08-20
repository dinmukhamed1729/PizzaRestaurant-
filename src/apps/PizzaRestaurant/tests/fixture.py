import pytest
from django.test import Client

from src.apps.PizzaRestaurant.models import Restaurant, Ingredient, Chef, Pizza
from src.apps.common.enums import Thickness


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(name="Test Resto", address="Almaty")


@pytest.fixture
def ingredient():
    return Ingredient.objects.create(name="Помидоры")


@pytest.fixture
def chef(restaurant: Restaurant):
    return Chef.objects.create(name="Test Chef", restaurant=restaurant)


@pytest.fixture
def pizza(restaurant: Restaurant, ingredient: Ingredient):
    pizza = Pizza.objects.create(
        name="Маргарита",
        cheese="моцарелла",
        thickness=Thickness.THIN,
        restaurant=restaurant
    )
    pizza.secret_ingredient.set([ingredient])
    return pizza
