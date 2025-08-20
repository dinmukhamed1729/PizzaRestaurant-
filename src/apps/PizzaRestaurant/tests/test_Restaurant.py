import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db(transaction=True)
def test_create_pizza_success(client: Client):
    from src.apps.PizzaRestaurant.models import Pizza, Ingredient, Restaurant
    from src.apps.common.enums import Thickness
    restaurant = Restaurant.objects.create(name="Test Resto", address="Almaty")
    ingredient = Ingredient.objects.create(name="Помидоры")

    payload = {
        "name": "Маргарита",
        "cheese": "моцарелла",
        "thickness": 'тонкое',
        "secret_ingredient": [ingredient.id],
        "restaurant_id": restaurant.id
    }

    url = "/api/pizzas/"
    response = client.post(url, payload, content_type="application/json")

    assert response.status_code == 200
    pizza = Pizza.objects.get(name="Маргарита")
    assert pizza.cheese == "моцарелла"
    assert pizza.thickness == Thickness.THIN
    assert ingredient in pizza.secret_ingredient.all()
