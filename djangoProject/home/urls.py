from django.urls import path, include
from .views import home
from users import*


urlpatterns = [
    # Map the root URL to the home view named 'home'
    path('', home, name='home'),
]