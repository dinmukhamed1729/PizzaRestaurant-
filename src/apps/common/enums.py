from enum import Enum

from django.db import models


class Thickness(models.TextChoices):
    THIN = "тонкое", "Тонкое"
    CLASSIC = "классическое", "Классическое"
    THICK = "пышное", "Пышное"



