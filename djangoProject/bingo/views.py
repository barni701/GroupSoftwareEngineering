from django.shortcuts import render
import random
# Create your views here.

def make_board(rows,cols):
    #5x5 = 25 challenges
    challenges = [
        "Challenge 1", "Challenge 2", "Challenge 3", "Challenge 4", "Challenge 5",
        "Challenge 6", "Challenge 7", "Challenge 8", "Challenge 9", "Challenge 10",
        "Challenge 11", "Challenge 12", "Challenge 13", "Challenge 14", "Challenge 15",
        "Challenge 16", "Challenge 17", "Challenge 18", "Challenge 19", "Challenge 20",
        "Challenge 21", "Challenge 22", "Challenge 23", "Challenge 24", "Challenge 25"
    ]
    challenges.reverse()
    array = []
    for x in range(rows):
        row = []
        for y in range(cols):
            challenge = challenges.pop()
            #status = random.choice([0, 1])
            status = 0
            row.append({"status": status, "challenge": challenge})
        array.append(row)

    # static board
    board = [
        [{"status": 0, "challenge": "Challenge 1"}, {"status": 1, "challenge": "Challenge 2"}, {"status": 1, "challenge": "Challenge 3"}, {"status": 1, "challenge": "Challenge 4"}, {"status": 1, "challenge": "Challenge 5"}],
        [{"status": 0, "challenge": "Challenge 6"}, {"status": 1, "challenge": "Challenge 7"}, {"status": 1, "challenge": "Challenge 8"}, {"status": 1, "challenge": "Challenge 9"}, {"status": 1, "challenge": "Challenge 10"}],
        [{"status": 0, "challenge": "Challenge 11"}, {"status": 1, "challenge": "Challenge 12"}, {"status": 1, "challenge": "Challenge 13"}, {"status": 1, "challenge": "Challenge 14"}, {"status": 1, "challenge": "Challenge 15"}],
        [{"status": 0, "challenge": "Challenge 16"}, {"status": 1, "challenge": "Challenge 17"}, {"status": 1, "challenge": "Challenge 18"}, {"status": 1, "challenge": "Challenge 19"}, {"status": 1, "challenge": "Challenge 20"}],
        [{"status": 0, "challenge": "Challenge 21"}, {"status": 1, "challenge": "Challenge 22"}, {"status": 1, "challenge": "Challenge 23"}, {"status": 1, "challenge": "Challenge 24"}, {"status": 1, "challenge": "Challenge 25"}]
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
