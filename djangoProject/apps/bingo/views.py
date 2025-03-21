# Authors: Yoav Shimoni, Adam Brooks

from django.shortcuts import render
from django.http import JsonResponse
from ..users.models import UserProfile
import random
# Create your views here.

def bingo_view(request):
    """ 
    Get the user's saved board, check it for a bingo, and display it.
    If the user does not have a board saved, generate a new one and save it.
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
        return render(request, 'base.html')


    # Check for bingo
    if(checkBingo(board)):
        print("BINGO!!!!")

    return render(request, 'bingo/bingo.html', {'board': board})

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


"""
@login_required
def mark_square(request):
    data = json.loads(request.body)
    challenge = int(data.get("challenge"))
    
    # Get user profile
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Get completed games from database
    completed = user_profile.completed_games if user_profile.completed_games else []
    
    # Add new challenge if not already completed
    if challenge not in completed:
        completed.append(challenge)
        user_profile.completed_games = completed
        user_profile.save()
        
    # Also update session for immediate feedback
    request.session["completed_challenges"] = completed
    
    return JsonResponse({"success": True})"
"""
