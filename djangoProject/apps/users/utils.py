from apps.users.models import UserProfile
from apps.battlepass.models import UserBattlePass
from django.utils import timezone

def add_xp(user, amount):
    """Adds XP to a user and updates Battle Pass if active."""
    user_profile = user.userprofile
    user_profile.add_experience(amount)  # Updates user XP

    # If the user has a Battle Pass, add XP there too
    user_battle_pass = UserBattlePass.objects.filter(user=user, battle_pass__end_date__gte=timezone.now()).first()
    if user_battle_pass:
        user_battle_pass.progress_points += amount
        if user_battle_pass.progress_points >= 100:
            user_battle_pass.progress_points -= 100
            user_battle_pass.current_tier += 1  # Level up battle pass
        user_battle_pass.save()
    
    user_profile.save()