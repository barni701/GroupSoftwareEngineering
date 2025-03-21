# Authors: Yoav Shimoni, Adam Brooks

from django.shortcuts import render
import random
# Create your views here.

def bingo_view(request):
    board = make_board(rows=5, cols=5)
    return render(request, 'bingo/bingo.html', {'board': board})

# Returns generated board variable with random integer values
# 4x4
def make_board(rows,cols):
    # status: complete or incomplete
    # challenge: the text displayed
    # url: links to the challenge page

    numbers = random.sample(range(1, 16+1), 16)
    board = [ [0]*4 for i in range(4)]
    for i in range(0,4):
        for j in range(0,4):
            challenge = numbers.pop()
            board[i][j] = {"status": bool(random.getrandbits(1)), "challenge": "Challenge "+str(challenge), "url": "/games/game" +str(challenge)+"/"}

    return board

# Checks the provided board for bingos. Returns True if bingo, False otherwise.
def checkBingo(board):

    # Check Rows
    for i in range(4):
        if all(board[i][j]["status"] == 1 for j in range(4)):
            return True

    # Check Cols
    for i in range(4):
        if all(board[j][i]["status"] == 1 for j in range(4)):
            return True

    # Check Leading Diagonal
    if all(board[i][i]["status"] == 1 for i in range(4)):
        return True

    # Check Anti-Diagonal
    if all(board[i][3 - i]["status"] == 1 for i in range(4)):
        return True

    return False

