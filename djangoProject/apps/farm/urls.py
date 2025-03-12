# apps/farm/urls.py
from django.urls import path
from .views import building_list, building_detail, upgrade_building, choose_starting_buildings, building_catalog, \
    building_template_detail, purchase_building

urlpatterns = [
    path('buildings/', building_list, name="building_list"),
    path('buildings/<int:building_id>/', building_detail, name="building_detail"),
    path('buildings/<int:building_id>/upgrade/', upgrade_building, name="upgrade_building"),
    path('start/', choose_starting_buildings, name="choose_starting_buildings"),
    path('catalog/', building_catalog, name="building_catalog"),
    path('catalog/<int:template_id>/', building_template_detail, name="building_template_detail"),
    path('catalog/<int:template_id>/purchase/', purchase_building, name="purchase_building"),
]