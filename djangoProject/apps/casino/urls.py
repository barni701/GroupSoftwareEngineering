from django.urls import path
from .views import *

urlpatterns = [
    path("", casino_home, name="casino_home"),
    path("dice/", play_dice, name="play_dice"),
    path("leaderboard/", green_fund_leaderboard, name="green_fund_leaderboard"),
    path("roulette", play_roulette, name="play_roulette"),
    path("blackjack/", play_blackjack, name="play_blackjack"),
    path("blackjack/<int:game_id>/", play_blackjack, name="play_blackjack"),
]