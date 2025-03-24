from django.urls import path
from .views import battle_pass_view, buy_premium_pass

urlpatterns = [
    path('', battle_pass_view, name='battlepass'),
    path('buy_premium/', buy_premium_pass, name='buy_premium_pass'),
]