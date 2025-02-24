from django.shortcuts import render

# Create your views here.

def home(request):
    # Render the 'home/home.html' template
    return render(request, 'home/home.html')
