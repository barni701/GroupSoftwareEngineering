from django.urls import path
from .views import *
from .views import mark_square_ajax
urlpatterns = [
    path('game1/', quiz_view, name='quiz_view'),
    path('game2/', recycle_sort, name='recycle_sort'),
    path('game3/', eco_runner , name='eco_runner'),
    path('game4/', eco_memory, name='eco_memory'),
    path('game5/', gps_game, name='gps_game'),
    path("mark-square/", mark_square_ajax, name="mark_square_ajax"),  # Add this line
]