from django.urls import path
from .views import home

urlpatterns = [
    # Map the root URL to the home view named 'home'
    path('', home, name='home'),
]