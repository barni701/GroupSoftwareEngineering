from django.urls import path
from . import views

urlpatterns = [
    # root to quiz
    path('', views.quiz_view, name='quiz'),  
]
