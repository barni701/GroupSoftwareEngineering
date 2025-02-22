from django.shortcuts import render
import random
# Create your views here.

def make_board(rows,cols):
    # status: complete or incomplete
    # challenge: the text displayed
    # url: links to the challenge page
    board = [
        [{"status": 0, "challenge": "Challenge 1", "url": "https://google.com"}, {"status": 0, "challenge": "Challenge 2", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 3", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 4", "url": "https://google.com"}],
        [{"status": 0, "challenge": "Challenge 5", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 6", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 7", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 8", "url": "https://google.com"}],
        [{"status": 0, "challenge": "Challenge 9", "url": "https://google.com"}, {"status": 0, "challenge": "Challenge 10", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 11", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 12", "url": "https://google.com"}],
        [{"status": 0, "challenge": "Challenge 13", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 14", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 15", "url": "https://google.com"}, {"status": 1, "challenge": "Challenge 16", "url": "https://google.com"}],
    ]
    return board

def bingo_view(request):
    board = make_board(rows=5, cols=5)
    return render(request, 'bingo.html', {'board': board})
