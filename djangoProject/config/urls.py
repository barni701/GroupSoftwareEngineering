"""
URL configuration for SoftwareDevProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.home.urls')),
    path("users/", include("apps.users.urls")),
    path("bingo/", include("apps.bingo.urls")),
    path("games/", include("apps.games.urls")),
    path('market/', include('apps.market.urls')),
    path("casino/", include("apps.casino.urls")),
    path("crates/", include("apps.crates.urls")),
    path("crafting/", include("apps.crafting.urls")),
    path('farm/', include('apps.farm.urls')),
    path("battlepass/", include("apps.battlepass.urls")),
    path("climate_duels/", include("apps.climate_duels.urls")),
    path("garden/", include("apps.garden.urls")),
    path("city_builder/", include("apps.city_builder.urls")),
]
