# In a file like clear_stocks.py within a management/commands folder
from django.core.management.base import BaseCommand
from apps.market.models import Investment, StockPriceHistory

class Command(BaseCommand):
    help = "Clear all stock-related data (Investments and StockPriceHistory)."

    def handle(self, *args, **options):
        Investment.objects.all().delete()
        StockPriceHistory.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Cleared all stock data."))