from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sustainability_rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('5.0'))
    current_stock_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('100.00'))
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='investments')
    shares = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name} ({self.shares} shares)"

class MarketEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateTimeField(auto_now_add=True)
    # Impact factor: e.g., 0.1 means a 10% boost, -0.1 a 10% drop.
    impact_factor = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.00'))
    # Event duration in minutes
    duration = models.PositiveIntegerField(default=60)
    # End time can be computed from event_date and duration; alternatively, you can store it explicitly.
    # Relate event to companies (optional)
    companies_affected = models.ManyToManyField('Company', blank=True, related_name='market_events')

    def is_active(self):
        # Determine if the event is still active based on its duration.
        elapsed = (timezone.now() - self.event_date).total_seconds() / 60.0
        return elapsed < self.duration

    def __str__(self):
        return self.title


class StockPriceHistory(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="price_history")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} at {self.date}: ${self.price}"