from decimal import Decimal
from .models import BlackjackGame, GreenFund, GreenFundContribution, RouletteGame

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DiceGame
from ..battlepass.utils import add_battle_pass_points
from ..battlepass.views import battle_pass_view
from ..users.models import UserProfile  # Assuming you store currency here
from ..users.utils import add_xp

@login_required
def casino_home(request):
    return render(request, "casino/casino_home.html")

@login_required
def play_dice(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        bet_amount = Decimal(request.POST.get("bet_amount"))
        bet_type = request.POST.get("bet_type")
        prediction = int(request.POST.get("prediction"))
        green_bet = "green_bet" in request.POST  # Check if Green Bet is selected

        # Validate bet amount
        if bet_amount <= 0:
            messages.error(request, "Invalid bet amount.")
            return redirect("play_dice")

        # Validate prediction based on bet type
        if bet_type == "exact":
            if prediction not in range(1, 7):
                messages.error(request, "Prediction must be between 1 and 6.")
                return redirect("play_dice")
        elif bet_type == "odd_even":
            if prediction not in [0, 1]:
                messages.error(request, "Prediction must be 0 for Even or 1 for Odd.")
                return redirect("play_dice")
        elif bet_type == "high_low":
            if prediction not in [0, 1]:
                messages.error(request, "Prediction must be 0 for Low or 1 for High.")
                return redirect("play_dice")

        # Green Bet Deduction
        green_donation = bet_amount * Decimal("0.10") if green_bet else Decimal("0.00")
        final_bet = bet_amount - green_donation

        # Ensure User has Enough Currency
        if not user_profile.deduct_currency(bet_amount, "Bet on Dice Game"):
            messages.error(request, "Insufficient balance!")
            return redirect("play_dice")

        # Process Green Fund Contribution
        if green_bet:
            GreenFund.add_donation(green_donation)
            GreenFundContribution.add_contribution(request.user, green_donation)

        # Create Dice Game Entry
        game = DiceGame.objects.create(
            user=request.user,
            bet_amount=final_bet,
            bet_type=bet_type,
            prediction=prediction
        )
        game.roll_dice()  # Roll the dice and set the result

        # Calculate winnings
        winnings = 0
        if game.win:
            winnings = final_bet * (6 if bet_type == "exact" else 2)
            user_profile.add_currency(winnings, "Winnings from Dice Game")
            xp_gain = max(10, min(bet_amount // 2, 100))  # XP scales with bet
            add_xp(request.user, xp_gain)
        else:
            xp_gain = max(5, min(bet_amount // 4, 50))  # XP for losing
            add_xp(request.user, xp_gain)

        # Game history and win percentage calculation
        all_games = DiceGame.objects.filter(user=request.user).order_by("-timestamp")
        total_games = all_games.count()
        wins = all_games.filter(win=True).count()
        win_percentage = (wins / total_games * 100) if total_games > 0 else 0

        game_history = all_games[:10]  # Get the last 10 games for display

        # Re-render the page with updated data
        return render(request, "casino/dice.html", {
            "game_history": game_history,
            "win_percentage": win_percentage,
            "green_fund_amount": GreenFund.objects.first().total_donated if GreenFund.objects.exists() else Decimal("0.00"),
            "roll_result": game.roll_result,  # Pass the roll_result to the template
            "winnings": winnings,
            "messages": f"🎉 You won ${winnings}!" if game.win else f"❌ You lost! Dice rolled {game.roll_result}.",
            "green_donation": str(green_donation) if green_bet else "0",
            "prediction": prediction,  # Pass prediction for display in history
            "bet_type": bet_type,  # Pass bet_type for display in history
            "bet_amount": bet_amount,  # Pass bet_amount to prefill the form
        })

    # Handle GET Requests (Render the Dice Page)
    all_games = DiceGame.objects.filter(user=request.user).order_by("-timestamp")
    total_games = all_games.count()
    wins = all_games.filter(win=True).count()
    win_percentage = (wins / total_games * 100) if total_games > 0 else 0

    return render(request, "casino/dice.html", {
        "game_history": all_games[:10],
        "win_percentage": win_percentage,
        "green_fund_amount": GreenFund.objects.first().total_donated if GreenFund.objects.exists() else Decimal("0.00")
    })

@login_required
def green_fund_leaderboard(request):
    """Display the top Green Fund contributors."""
    top_contributors = GreenFundContribution.objects.order_by("-total_donated")[:10]
    return render(request, "casino/leaderboard.html", {"top_contributors": top_contributors})


@login_required
def play_roulette(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        bet_amount = Decimal(request.POST.get("bet_amount"))
        bet_type = request.POST.get("bet_type")
        prediction = request.POST.get("prediction").strip()  # prediction as string
        green_bet = "green_bet" in request.POST  # Green Bet checkbox

        # Validate bet amount
        if bet_amount <= 0:
            messages.error(request, "Invalid bet amount.")
            return redirect("play_roulette")

        # Validate prediction based on bet type
        if bet_type == "number":
            try:
                num = int(prediction)
                if num < 0 or num > 36:
                    messages.error(request, "For a number bet, enter a number between 0 and 36.")
                    return redirect("play_roulette")
            except ValueError:
                messages.error(request, "For a number bet, please enter a valid number.")
                return redirect("play_roulette")
        elif bet_type == "color":
            if prediction.lower() not in ["red", "black"]:
                messages.error(request, "For a color bet, enter 'red' or 'black'.")
                return redirect("play_roulette")
        elif bet_type == "odd_even":
            if prediction.lower() not in ["odd", "even"]:
                messages.error(request, "For an odd/even bet, enter 'odd' or 'even'.")
                return redirect("play_roulette")
        elif bet_type == "low_high":
            if prediction.lower() not in ["low", "high"]:
                messages.error(request, "For a low/high bet, enter 'low' or 'high'.")
                return redirect("play_roulette")

        # Deduct full bet amount from user currency
        if not user_profile.deduct_currency(bet_amount, "Bet on Roulette"):
            messages.error(request, "Insufficient balance!")
            return redirect("play_roulette")

        # If Green Bet, process donation: deduct 10% of bet for donation.
        green_donation = bet_amount * Decimal("0.10") if green_bet else Decimal("0.00")
        final_bet = bet_amount - green_donation
        if green_bet:
            GreenFund.add_donation(green_donation)
            GreenFundContribution.add_contribution(request.user, green_donation)

        # Create and play a roulette game
        roulette_game = RouletteGame.objects.create(
            user=request.user,
            bet_amount=final_bet,
            bet_type=bet_type,
            prediction=prediction
        )
        roulette_game.play()

        # Calculate winnings using the final bet (the actual wager)
        winnings = 0
        win = False
        if roulette_game.win:
            win = True
            if bet_type == "number":
                winnings = final_bet * 36  # You receive 36x your wager; net profit is 35x.
            else:
                winnings = final_bet * 2  # Even money bet: 2x your wager; net profit is equal to your wager.
            user_profile.add_currency(winnings, "Winnings from Roulette")
            xp_gain = max(10, min(bet_amount // 2, 100))  # XP scales with bet
            add_xp(request.user, xp_gain)
        else:
            xp_gain = max(5, min(bet_amount // 4, 50))  # XP for losing
            add_xp(request.user, xp_gain)

        # Refresh user profile to get updated balance
        user_profile.refresh_from_db()
        updated_balance = user_profile.currency_balance

        # Get updated green fund amount
        green_fund = GreenFund.objects.first()
        updated_green_fund = green_fund.total_donated if green_fund else Decimal("0.00")

        # Get game history and win percentage
        all_games = RouletteGame.objects.filter(user=request.user).order_by("-timestamp")
        total_games = all_games.count()
        wins = all_games.filter(win=True).count()
        win_percentage = (wins / total_games * 100) if total_games > 0 else 0

        game_history = all_games[:10]

        return render(request, "casino/roulette.html", {
            "game_history": game_history,
            "win_percentage": win_percentage,
            "green_fund_amount": updated_green_fund,
            "roll_result": roulette_game.result,
            "winnings": winnings,
            "messages": f"🎉 You won {winnings} currency!" if roulette_game.win else f"❌ You lost! Roulette result: {roulette_game.result}.",
            "green_donation": str(green_donation) if green_bet else "0",
            "user_balance": updated_balance,
            "bet_type": bet_type,
            "prediction": prediction,
            "bet_amount": bet_amount,
            "win": win,
        })

    # For GET requests, render page with current data
    all_games = RouletteGame.objects.filter(user=request.user).order_by("-timestamp")
    total_games = all_games.count()
    wins = all_games.filter(win=True).count()
    win_percentage = (wins / total_games * 100) if total_games > 0 else 0

    user_profile.refresh_from_db()
    updated_balance = user_profile.currency_balance
    green_fund = GreenFund.objects.first()
    updated_green_fund = green_fund.total_donated if green_fund else Decimal("0.00")

    return render(request, "casino/roulette.html", {
        "game_history": all_games[:10],
        "win_percentage": win_percentage,
        "green_fund_amount": updated_green_fund,
        "user_balance": updated_balance,
    })

@login_required
def play_blackjack(request, game_id=None):
    # Load an existing game if provided, else None.
    if game_id:
        game = get_object_or_404(BlackjackGame, id=game_id, user=request.user)
    else:
        game = None

    if request.method == "POST":
        action = request.POST.get("action")
        # If no game exists, create a new game.
        if not game:
            bet_amount = Decimal(request.POST.get("bet_amount", "0"))
            if bet_amount <= 0:
                messages.error(request, "Invalid bet amount.")
                return redirect("casino_home")
            user_profile = request.user.userprofile
            if not user_profile.deduct_currency(bet_amount, "Bet on Blackjack"):
                messages.error(request, "Insufficient funds.")
                return redirect("casino_home")
            game = BlackjackGame.objects.create(user=request.user, bet_amount=bet_amount)
            game.initialize_game()

        # Process player action.
        if action == "hit":
            game.hit()
            if game.player_value() > 21:
                game.determine_result()
                messages.info(request, "Bust! You lost.")
        elif action == "stand":
            game.dealer_play()
            game.determine_result()
            messages.info(request, f"Game over. You {game.result}.")
        elif action == "double":
            # Allow doubling only if exactly 2 cards in player's hand.
            if len(game.player_hand) != 2:
                messages.error(request, "You can only double down on your first move (with exactly 2 cards).")
                return redirect("play_blackjack", game_id=game.id)
            extra_bet = game.bet_amount
            user_profile = request.user.userprofile
            if not user_profile.deduct_currency(extra_bet, "Double down on Blackjack"):
                messages.error(request, "Insufficient funds to double down.")
                return redirect("play_blackjack", game_id=game.id)
            game.bet_amount += extra_bet
            game.save()
            game.hit()
            game.dealer_play()
            game.determine_result()
            messages.info(request, f"Double down complete. You {game.result}.")

        # Award XP (using your centralized XP function)
        xp_gain = game.bet_amount * Decimal("10")  # Example: 10 XP per bet unit.
        add_xp(request.user, xp_gain)

        # Award currency based on game result:
        user_profile = request.user.userprofile
        if game.result == "win":
            # For a win, pay out 2x the bet (refund plus winnings).
            winnings = game.bet_amount * Decimal("2")
            user_profile.add_currency(winnings, description="Blackjack win payout")
            messages.success(request, f"You win! You earned ${winnings}.")
        elif game.result == "push":
            # Refund the bet if it's a push.
            user_profile.add_currency(game.bet_amount, description="Blackjack push refund")
            messages.info(request, "Push! Your bet has been refunded.")
        # For a loss, no currency is added.
        
        return redirect("play_blackjack", game_id=game.id)

    return render(request, "casino/blackjack.html", {"game": game})