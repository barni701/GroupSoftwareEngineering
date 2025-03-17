from django.urls import path
from .views import (
    add_city_funds,
    city_dashboard,
    building_catalog,
    building_template_detail,
    collect_production,
    construct_building,
    material_dashboard,
    upgrade_building,
)

urlpatterns = [
    path('', city_dashboard, name="city_dashboard"),
    path('catalog/', building_catalog, name="building_catalog"),
    path('template/<int:template_id>/', building_template_detail, name="building_template_detail"),
    path('construct/<int:template_id>/', construct_building, name="construct_building"),
    path('upgrade/<int:building_id>/', upgrade_building, name="upgrade_building"),
    path('add_funds/', add_city_funds, name="add_city_funds"),
    path('collect/<int:building_id>/', collect_production, name="collect_production"),
    path('materials/', material_dashboard, name="material_dashboard"),
]