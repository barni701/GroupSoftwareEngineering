from datetime import timedelta

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
    impact_factor = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.00'))
    duration = models.PositiveIntegerField(default=60)  # in minutes
    companies_affected = models.ManyToManyField(Company, related_name="market_events")

    def get_time_left(self):
        end_time = self.event_date + timedelta(minutes=self.duration)
        now = timezone.now()
        if now < end_time:
            remaining = end_time - now
            minutes = int(remaining.total_seconds() // 60)
            return f"{minutes} minutes left"
        else:
            return "Expired"

    def is_active(self):
        end_time = self.event_date + timedelta(minutes=self.duration)
        return timezone.now() < end_time

    @property
    def end_timestamp(self):
        # Convert event_date to Unix timestamp and add duration (converted to seconds)
        return int(self.event_date.timestamp() + self.duration * 60)

    def __str__(self):
        return self.title


class StockPriceHistory(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="price_history")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} at {self.date}: ${self.price}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    shares = models.PositiveIntegerField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.shares} shares of {self.company.name} at {self.timestamp}"

class PortfolioSnapshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_snapshots')
    total_value = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.total_value} at {self.timestamp}"

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    threshold = models.DecimalField(max_digits=12, decimal_places=2, help_text="Value or score needed to earn this achievement")
    # For example, threshold might represent a portfolio value or a green impact score

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"