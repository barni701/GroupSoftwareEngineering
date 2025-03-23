# Authors: Yoav Shimoni, Adam Brooks

from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..users.models import UserProfile
import random
# Create your views here.

def bingo_view(request):
    """ 
    Get the user's saved board, check it for a bingo, and display it.
    If the user does not have a board saved, generate a new one and save it.
    If the user is not logged in, redirect them to login page
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        board = user_profile.bingo_board
        print(board)
        if(board == []):
            # If the user doesnt have a board, generate a new one and save it to their profile
            board = newUser()
            user_profile.bingo_board = board
            user_profile.save()
    except:
        print("User is not logged in!")
        return redirect('http://127.0.0.1:8000/users/login?next=bingo')


    # Check for and pass bingo to html
    bingo = checkBingo(board)
    if(bingo):
            # Generate New Board
            board = newUser()
            user_profile.bingo_board = board
            user_profile.save()
    return render(request, 'bingo/bingo.html', {'board': board, 'bingo': bingo})

# Returns generated board variable with random integer values
# 4x4
def make_board(rows,cols):
    # status: BOOL, complete or incomplete
    # challenge: STRING, the text displayed
    # url: STRING, links to the challenge page

    numbers = random.sample(range(1, 16+1), 16)
    board = [ [0]*4 for i in range(4)]
    for i in range(0,4):
        for j in range(0,4):
            challenge = numbers.pop()
            board[i][j] = {"status": False, "challenge": "Challenge "+str(challenge), "url": "/games/game" +str(challenge)+"/"}

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

def newUser():
    # TODO: Create popup with info about game
    return make_board(rows=5, cols=5)
