from .views import bingo_view
from django.urls import path

urlpatterns = [
    path('', bingo_view, name='bingo'),
]