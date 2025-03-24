from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.users.models import UserProfile
from apps.market.models import Investment, PortfolioSnapshot

class Command(BaseCommand):
    help = "Record a snapshot of each user's portfolio value"

    def handle(self, *args, **options):
        profiles = UserProfile.objects.all()
        for profile in profiles:
            investments = Investment.objects.filter(user=profile.user)
            total_value = Decimal('0.00')
            for inv in investments:
                total_value += inv.company.current_stock_price * inv.shares
            # Create a snapshot record
            snapshot = PortfolioSnapshot.objects.create(
                user=profile.user,
                total_value=total_value
            )
            self.stdout.write(self.style.SUCCESS(
                f"Recorded snapshot for {profile.user.username}: ${snapshot.total_value}"
            ))