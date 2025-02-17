from django.shortcuts import render
import random
# Create your views here.

def make_board(rows,cols):
    # static board
    board = [
        [{"status": 0, "challenge": "Challenge 1"}, {"status": 0, "challenge": "Challenge 2"}, {"status": 1, "challenge": "Challenge 3"}, {"status": 1, "challenge": "Challenge 4"}],
        [{"status": 0, "challenge": "Challenge 5"}, {"status": 1, "challenge": "Challenge 6"}, {"status": 1, "challenge": "Challenge 7"}, {"status": 1, "challenge": "Challenge 8"}],
        [{"status": 0, "challenge": "Challenge 9"}, {"status": 0, "challenge": "Challenge 10"}, {"status": 1, "challenge": "Challenge 11"}, {"status": 1, "challenge": "Challenge 12"}],
        [{"status": 0, "challenge": "Challenge 13"}, {"status": 1, "challenge": "Challenge 14"}, {"status": 1, "challenge": "Challenge 15"}, {"status": 1, "challenge": "Challenge 16"}],
    ]
    return board
    #return array

def bingo_view(request):
    board = make_board(rows=5, cols=5)
    '''
    board = [
    [1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
    ]
    '''
    return render(request, 'bingo.html', {'board': board})
