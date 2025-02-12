from django.shortcuts import render

# Create your views here.
def bingo_view(request):
    return render(request, 'bingo.html')
