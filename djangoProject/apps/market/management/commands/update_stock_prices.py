import random
from decimal import Decimal, ROUND_HALF_UP
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.market.models import Company, StockPriceHistory, MarketEvent


class Command(BaseCommand):
    help = "Update stock prices for all companies with improved simulation"

    def handle(self, *args, **options):
        companies = Company.objects.all()
        for company in companies:
            # 1. Base fluctuation: random change between -2% and +2%
            base_change = Decimal(random.uniform(-0.02, 0.02)).quantize(
                Decimal('0.0001'), rounding=ROUND_HALF_UP
            )

            # 2. Mean reversion: assume a target price (e.g., $100) and add a correction factor
            target_price = Decimal('100.00')
            mean_reversion_strength = Decimal('0.01')  # 1% correction factor
            mean_reversion = ((target_price - company.current_stock_price) / target_price) * mean_reversion_strength

            # 3. Event impact: sum of impact factors from all active events affecting this company
            active_events = company.market_events.filter(event_date__lte=timezone.now())
            total_event_impact = Decimal('0.00')
            for event in active_events:
                if event.is_active():
                    total_event_impact += event.impact_factor

            # Calculate net percentage change
            net_percentage_change = base_change + mean_reversion + total_event_impact

            old_price = company.current_stock_price
            # New price is old_price multiplied by (1 + net percentage change)
            new_price = (old_price * (Decimal('1.00') + net_percentage_change)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

            # Ensure the price doesn't drop below a minimum threshold, e.g., $1.00
            if new_price < Decimal('1.00'):
                new_price = Decimal('1.00')

            # Update company and create historical record
            company.current_stock_price = new_price
            company.save()
            StockPriceHistory.objects.create(company=company, price=new_price)

            self.stdout.write(self.style.SUCCESS(
                f"Updated {company.name}: ${old_price} -> ${new_price} "
                f"(Base: {base_change}, Mean Reversion: {mean_reversion}, Event: {total_event_impact})"
            ))