from .models import UserBattlePass, BattlePass
from django.utils import timezone


def initialize_user_battle_pass(user):
    """Ensure a user has only ONE active battle pass per season."""
    active_battle_pass = BattlePass.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).first()

    if not active_battle_pass:
        return None  # No active battle pass

    # Ensure there’s only one entry
    user_battle_pass = UserBattlePass.objects.filter(
        user=user, battle_pass=active_battle_pass
    ).order_by('-id').first()  # Get the latest one if duplicates exist

    if not user_battle_pass:
        user_battle_pass = UserBattlePass.objects.create(
            user=user,
            battle_pass=active_battle_pass,
            current_tier=0,
            progress_points=0
        )

    return user_battle_pass

def add_battle_pass_points(user, points):
    """Add points to the user's active battle pass and allow multi-tier progression."""
    user_battle_pass = initialize_user_battle_pass(user)

    if user_battle_pass:
        user_battle_pass.progress_points += points
        user_battle_pass.progress_to_next_tier()  # ✅ Now accounts for multiple level-ups
