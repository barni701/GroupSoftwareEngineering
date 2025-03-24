import random
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User  # Using built-in User
from apps.market.models import Company, Investment

# Set threshold: if a company's stock remains below $1.50 for more than 2 minutes.
THRESHOLD_DURATION = timedelta(minutes=2)
# Define a baseline reset price
RESET_PRICE = Decimal("100.00")
# Price threshold for triggering the reset
PRICE_THRESHOLD = Decimal("1.50")


class Command(BaseCommand):
    help = "Reset a stock's value and remove investments if the stock price remains below $1.50 for more than two minutes."

    def handle(self, *args, **options):
        now = timezone.now()
        # Find companies with current_stock_price less than $1.50
        companies = Company.objects.filter(current_stock_price__lt=PRICE_THRESHOLD)
        if not companies.exists():
            self.stdout.write("No companies found with stock price below $1.50.")
            return

        for company in companies:
            if company.price_low_since and (now - company.price_low_since) >= THRESHOLD_DURATION:
                self.stdout.write(
                    f"Resetting {company.name}: Price has been below $1.50 for {(now - company.price_low_since)}.")

                # Retrieve all investments for this company
                investments = Investment.objects.filter(company=company)
                total_shares = sum(inv.shares for inv in investments)
                investments.delete()

                # Log affected users using the related name 'investments'
                affected_users = User.objects.filter(investments__company=company).distinct()
                for user in affected_users:
                    self.stdout.write(f"User {user.username} had investments in {company.name} removed.")

                # Reset the company's stock price and clear the price_low_since flag.
                company.current_stock_price = RESET_PRICE
                company.price_low_since = None
                company.save()

                self.stdout.write(self.style.SUCCESS(
                    f"Reset {company.name} to ${RESET_PRICE} and removed investments totaling {total_shares} shares."
                ))
            else:
                self.stdout.write(f"{company.name} is below $1.50 but hasn't been for 2 minutes yet.")
        self.stdout.write(self.style.SUCCESS("Stock price reset process complete."))