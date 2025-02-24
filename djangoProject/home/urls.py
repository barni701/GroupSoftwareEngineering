from django.urls import path, include
from .views import home
from users import*

urlpatterns = [
    path('', home, name='home'),
]