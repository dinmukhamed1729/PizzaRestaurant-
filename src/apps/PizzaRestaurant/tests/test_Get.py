from src.apps.PizzaRestaurant.models import Review
from src.apps.PizzaRestaurant.tests.fixture import *



@pytest.mark.django_db(transaction=True)
def test_get_restaurants(client: Client, restaurant: Restaurant):
    url = "/api/restaurants/"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.django_db(transaction=True)
def test_get_chefs(client: Client, chef: Chef):
    url = "/api/chefs/"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.django_db(transaction=True)
def test_get_pizzas(client: Client, pizza: Pizza):
    url = "/api/pizzas/"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.django_db(transaction=True)
def test_get_ingredients(client: Client, ingredient: Ingredient):
    url = "/api/ingredients/"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.django_db(transaction=True)
def test_get_reviews(client: Client):
    restaurant = Restaurant.objects.create(name="Resto4", address="Almaty")
    Review.objects.create(rating=5, feedback="Отлично", restaurant=restaurant)
    url = "/api/reviews/"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) >= 1
