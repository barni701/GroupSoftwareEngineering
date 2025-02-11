from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is my new Django app!")