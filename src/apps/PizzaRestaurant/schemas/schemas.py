from typing import List, Optional

from ninja import ModelSchema, Field, Schema

from src.apps.PizzaRestaurant.models import Chef, Restaurant, Pizza, Ingredient, Review


class ChefSchema(ModelSchema):
    class Config:
        model = Chef
        model_fields = ['name']


class RestaurantSchema(ModelSchema):
    class Config:
        model = Restaurant
        model_fields = ['name', 'address']


class ChefInSchema(ChefSchema):
    restaurant_id: int


class ChefNestedSchema(ChefSchema):
    id: int


class RestaurantOutSchema(RestaurantSchema):
    id: int
    chef: ChefNestedSchema | None = None


class RestaurantNestedSchema(RestaurantSchema):
    id: int


class ChefOutSchema(ChefSchema):
    id: int
    restaurant: RestaurantNestedSchema | None = None


class IngredientSchema(ModelSchema):
    class Config:
        model = Ingredient
        model_fields = ['name']


class IngredientOutSchema(IngredientSchema):
    id: int


class PizzaSchema(ModelSchema):
    class Config:
        model = Pizza
        model_fields = ['name', 'cheese', 'thickness', 'secret_ingredient']


class PizzaPatchSchema(Schema):
    name: Optional[str] = None
    cheese: Optional[str] = None
    thickness: Optional[str] = None
    secret_ingredient: Optional[List[int]] = None


class PizzaNestedSchema(ModelSchema):
    class Config:
        model = Pizza
        model_fields = ['name', 'cheese', 'thickness']

    secret_ingredient: List[IngredientOutSchema] | None = None


class PizzaInSchema(PizzaSchema):
    restaurant_id: int


class PizzaOutSchema(PizzaSchema):
    id: int
    restaurant: RestaurantNestedSchema | None = None


class ReviewSchema(ModelSchema):
    rating: int = Field(..., ge=1, le=5)

    class Config:
        model = Review
        model_fields = ['feedback']


class ReviewOutSchema(ReviewSchema):
    id: int
    restaurant: RestaurantNestedSchema | None = None


class ReviewInSchema(ReviewSchema):
    restaurant_id: int


class RestaurantMenuSchema(RestaurantOutSchema):
    pizzas: list[PizzaNestedSchema]
