from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserBattlePass, BattlePassTier
from django.utils import timezone

from .utils import initialize_user_battle_pass

@login_required
def battle_pass_leaderboard(request):
    leaderboard = UserBattlePass.objects.order_by('-current_tier', '-progress_points')[:10]
    return render(request, "battlepass/leaderboard.html", {"leaderboard": leaderboard})

@login_required
def buy_premium_pass(request):
    user_battle_pass = UserBattlePass.objects.filter(
        user=request.user, battle_pass__end_date__gte=timezone.now()
    ).first()

    if not user_battle_pass:
        messages.error(request, "You don't have an active Battle Pass.")
        return redirect('battlepass')

    # Define the cost of the premium pass
    PREMIUM_COST = 1000

    if request.user.userprofile.currency_balance < PREMIUM_COST:
        messages.error(request, "You don't have enough currency to buy the premium pass.")
        return redirect('battlepass')

    # Deduct cost and activate premium
    request.user.userprofile.currency_balance -= PREMIUM_COST
    request.user.userprofile.save()
    user_battle_pass.has_premium = True
    user_battle_pass.save()

    messages.success(request, "Premium Battle Pass activated! Enjoy exclusive rewards.")
    return redirect('battlepass')

@login_required
def battle_pass_view(request):
    user_battle_pass = initialize_user_battle_pass(request.user)

    if user_battle_pass:
        tiers = BattlePassTier.objects.filter(battle_pass=user_battle_pass.battle_pass).order_by("tier_level")
    else:
        tiers = []

    return render(request, "battlepass/battlepass.html", {
        "user_battle_pass": user_battle_pass,
        "tiers": tiers,
    })

def grant_reward(user, reward):
    """Grant a reward to a user."""
    user_profile = user.userprofile
    if reward.reward_type == 'currency':
        user_profile.currency_balance += reward.reward_value
        user_profile.save()
    elif reward.reward_type == 'item':
        # Implement inventory system reward logic
        pass
    elif reward.reward_type == 'badge':
        # Implement badge system logic
        pass