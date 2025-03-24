from decimal import Decimal
from apps.market.models import Investment, PortfolioSnapshot, Achievement, UserAchievement


def record_portfolio_snapshot(user):
    investments = Investment.objects.filter(user=user)
    total_value = Decimal('0.00')
    for inv in investments:
        total_value += inv.company.current_stock_price * inv.shares
    # Create a snapshot record for the user's portfolio
    PortfolioSnapshot.objects.create(user=user, total_value=total_value)

def check_and_award_achievements(user, portfolio_data):
    """
    Checks user's portfolio metrics against achievement thresholds
    and awards achievements if not already earned.
    """
    # For example, let's say we have two types of achievements:
    # - Portfolio Value Achievement: threshold is based on current portfolio value.
    # - Green Impact Achievement: threshold is based on green impact score.
    total_value = sum(item['current_amount'] for item in portfolio_data)
    green_impact = sum(item['company'].sustainability_rating * item['shares'] for item in portfolio_data)

    # Retrieve achievements (you can have more sophisticated logic and different achievement types)
    portfolio_value_achievements = Achievement.objects.filter(name__icontains="Portfolio Value")
    green_impact_achievements = Achievement.objects.filter(name__icontains="Green Impact")

    # Award portfolio value achievements if threshold is met
    for achievement in portfolio_value_achievements:
        if total_value >= achievement.threshold:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)

    # Award green impact achievements if threshold is met
    for achievement in green_impact_achievements:
        if green_impact >= achievement.threshold:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)