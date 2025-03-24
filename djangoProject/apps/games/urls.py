from django.urls import path
from .views import *
from .views import mark_square_ajax
urlpatterns = [
    path('game1/', quiz_view, name='quiz_view'),
    path('game2/', recycle_sort, name='recycle_sort'),
    path('game3/', eco_runner , name='eco_runner'),
    path('game4/', eco_memory, name='eco_memory'),
    path('game5/', gps_game, name='gps_game'),
    path('game6/', gps_game2, name='gps_game2'),
    path('game7/', gps_game3, name='gps_game3'),
    path('game8/', gps_game4, name='gps_game4'),
    path('game9/', gps_game5, name='gps_game5'),
    path("mark-square/", mark_square_ajax, name="mark_square_ajax"), 
]