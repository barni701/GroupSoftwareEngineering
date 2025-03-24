from decimal import Decimal

def has_made_first_deposit(profile):
    return profile.currency_balance > Decimal('0.00')

def has_reached_level_5(profile):
    return profile.level >= 5

def has_reached_level_10(profile):
    return profile.level >= 10

def has_opened_10_crates(profile):
    return profile.total_crates_opened >= 10

def has_earned_1000_currency(profile):
    return profile.currency_balance >= Decimal('1000.00')

def has_added_a_friend(profile):
    return profile.friends.count() > 0

def has_crafted_first_item(profile):
    return profile.items_crafted > 0

def has_logged_in_seven_days(profile):
    return profile.login_streak >= 7

def has_played_all_games(profile):
    return profile.games_played >= 5  # Example threshold

# Additional achievement condition functions can be added here.

ACHIEVEMENT_CONDITIONS = {
    'First Deposit': has_made_first_deposit,
    'Level 5 Reached': has_reached_level_5,
    'Level 10 Reached': has_reached_level_10,
    'Crate Opener': has_opened_10_crates,
    'Thousandaire': has_earned_1000_currency,
    'Social Starter': has_added_a_friend,
    'First Crafter': has_crafted_first_item,
    'Weekly Regular': has_logged_in_seven_days,
    'Game Explorer': has_played_all_games,
    # Add more achievements as needed.
}