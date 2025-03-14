from django.urls import path
from . import views

app_name = "climate_duels"

urlpatterns = [
    path("", views.duel_list, name="duel_list"),
    path("create/", views.create_duel, name="create_duel"),
    path("join/<int:duel_id>/", views.join_duel, name="join_duel"),
    path("play/<int:duel_id>/", views.play_turn, name="play_turn"),
    path("results/<int:duel_id>/", views.duel_results, name="duel_results"),  # ✅ Results Page
]