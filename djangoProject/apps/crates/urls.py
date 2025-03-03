from django.urls import path
from . import views

urlpatterns = [
    path('', views.crate_inventory, name="crate_inventory"),
    path('open/<int:crate_id>/', views.open_crate, name="open_crate"),
    path('history/', views.crate_history, name="crate_history"),
    path('shop/', views.crate_shop, name="crate_shop"),
    path('buy/<str:crate_type>/', views.buy_crate, name="buy_crate"),
]