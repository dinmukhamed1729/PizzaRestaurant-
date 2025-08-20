"""
URL configuration for src project.

The `urlpatterns` list routes URLs to api. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function api
    1. Add an import:  from my_app import api
    2. Add a URL to urlpatterns:  path('', api.home, name='home')
Class-based api
    1. Add an import:  from other_app.api import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from src.config.api import (
    api_restaurant
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_restaurant.urls, name='api-restaurant'),

]
