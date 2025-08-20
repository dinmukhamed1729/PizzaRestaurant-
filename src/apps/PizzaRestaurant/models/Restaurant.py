from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q

from src.apps.common.enums import Thickness
from src.apps.common.model import BaseModel


class Restaurant(BaseModel):
    class Meta:
        db_table = 'restaurant'

    name = models.CharField(
        max_length=255,
        unique=True
    )
    address = models.CharField(
        max_length=255
    )


class Chef(BaseModel):
    class Meta:
        db_table = 'chefs'

    restaurant = models.OneToOneField(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='chef'
    )
    name = models.CharField(max_length=255)


class Ingredient(BaseModel):
    class Meta:
        db_table = 'ingredients'

    name = models.CharField(
        max_length=255,
        unique=True
    )


class Pizza(BaseModel):
    class Meta:
        db_table = 'pizzas'
        constraints = [
            models.CheckConstraint(
                check=Q(thickness__in=[c.value for c in Thickness]),
                name="pizza_thickness_valid"
            )
        ]

    name = models.CharField(
        max_length=255,
    )
    cheese = models.CharField(
        max_length=255
    )
    thickness = models.CharField(
        max_length=20,
        choices=Thickness.choices,
        default=Thickness.CLASSIC
    )
    secret_ingredient = models.ManyToManyField(
        Ingredient,
        related_name='ingredients'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='pizzas'
    )


class Review(BaseModel):
    class Meta:
        db_table = 'reviews'

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    feedback = models.TextField()
