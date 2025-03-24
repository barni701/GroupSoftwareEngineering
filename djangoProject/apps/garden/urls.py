from django.urls import path
from .views import garden_dashboard, available_seeds, plant_seed, create_plot, harvest_crop

urlpatterns = [
    path('', garden_dashboard, name="garden_dashboard"),
    path('seeds/<int:plot_id>/', available_seeds, name="available_seeds"),
    path('plant/<int:plot_id>/<int:seed_id>/', plant_seed, name="plant_seed"),
    path('create/', create_plot, name="create_plot"),
    path('harvest/<int:plant_id>/', harvest_crop, name="harvest_crop"),
]