# game1/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view, name='quiz'),  # The root path for the quiz
]
