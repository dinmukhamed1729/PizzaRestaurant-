from src.apps.PizzaRestaurant.tests.fixture import *
from django.test import Client


@pytest.mark.django_db(transaction=True)
def test_delete_pizza(client: Client, pizza: Pizza):
    url = f"/api/pizzas/{pizza.id}/"
    response = client.delete(url)
    assert response.status_code == 200
    assert not Pizza.objects.filter(id=pizza.id).exists()


@pytest.mark.django_db(transaction=True)
def test_delete_chef(client: Client, chef: Chef):
    url = f"/api/chefs/{chef.id}/"
    response = client.delete(url)
    assert response.status_code == 200
    assert not Chef.objects.filter(id=chef.id).exists()


@pytest.mark.django_db(transaction=True)
def test_delete_restaurant(client: Client, restaurant: Restaurant):
    url = f"/api/restaurants/{restaurant.id}/"
    response = client.delete(url)
    assert response.status_code == 200
    assert not Restaurant.objects.filter(id=restaurant.id).exists()
