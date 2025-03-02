from django.core.management import call_command
from celery import shared_task



@shared_task
def update_stock_prices_task():
    call_command('update_stock_prices')

@shared_task
def generate_market_event_task():
    call_command('generate_market_events')

@shared_task
def record_portfolio_snapshots_task():
    # Import models here to ensure Django apps are loaded
    from apps.users.models import UserProfile
    from apps.market.models import Investment, PortfolioSnapshot
    from decimal import Decimal

    profiles = UserProfile.objects.all()
    for profile in profiles:
        investments = Investment.objects.filter(user=profile.user)
        total_value = Decimal('0.00')
        for inv in investments:
            total_value += inv.company.current_stock_price * inv.shares
        PortfolioSnapshot.objects.create(user=profile.user, total_value=total_value)