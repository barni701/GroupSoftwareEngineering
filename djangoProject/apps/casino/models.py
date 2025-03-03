from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
import random

from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
import random

class DiceGame(models.Model):
    BET_TYPES = [
        ('exact', 'Exact Number'),
        ('odd_even', 'Odd or Even'),
        ('high_low', 'High or Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet_amount = models.DecimalField(max_digits=12, decimal_places=2)
    bet_type = models.CharField(max_length=10, choices=BET_TYPES, default='exact')
    prediction = models.IntegerField(null=True, blank=True)
    roll_result = models.IntegerField(null=True, blank=True)
    win = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def roll_dice(self):
        """Simulate a dice roll and determine the outcome."""
        self.roll_result = random.randint(1, 6)
        if self.bet_type == 'exact':
            self.win = self.roll_result == self.prediction
        elif self.bet_type == 'odd_even':
            self.win = (self.roll_result % 2 == 0) if self.prediction == 0 else (self.roll_result % 2 != 0)
        elif self.bet_type == 'high_low':
            self.win = (self.roll_result > 3) if self.prediction == 1 else (self.roll_result <= 3)
        self.save()

class GreenFund(models.Model):
    total_donated = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    @classmethod
    def add_donation(cls, amount):
        """Increase the total green fund by a given amount."""
        from django.db import transaction  # Ensure safe updates

        amount = Decimal(amount)
        with transaction.atomic():  # Ensure atomic updates
            fund, created = cls.objects.get_or_create(id=1)
            print(f"🌱 Adding donation: {amount} (Before: {fund.total_donated})")  # Debugging
            fund.total_donated += amount
            fund.save()
            print(f"✅ Updated Green Fund: {fund.total_donated}")  # Debugging

class GreenFundContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_donated = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    @classmethod
    def add_contribution(cls, user, amount):
        """Log user contributions to the Green Fund."""
        from django.db import transaction

        with transaction.atomic():
            contribution, created = cls.objects.get_or_create(user=user)
            contribution.total_donated += Decimal(amount)
            contribution.save()


class RouletteGame(models.Model):
    BET_TYPES = [
        ('number', 'Number'),
        ('color', 'Color'),
        ('odd_even', 'Odd/Even'),
        ('low_high', 'Low/High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet_amount = models.DecimalField(max_digits=12, decimal_places=2)
    bet_type = models.CharField(max_length=10, choices=BET_TYPES, default='number')
    prediction = models.CharField(max_length=10,
                                  help_text="Enter your prediction (e.g. a number, red/black, odd/even, low/high)")
    result = models.CharField(max_length=10, blank=True, null=True)  # outcome of roulette
    win = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def play(self):
        # European roulette: numbers 0-36; 0 is green.
        outcomes = [str(i) for i in range(0, 37)]
        self.result = random.choice(outcomes)

        # Define red and black numbers (0 is green)
        red_numbers = {"1", "3", "5", "7", "9", "12", "14", "16", "18", "19", "21", "23", "25", "27", "30", "32", "34",
                       "36"}
        black_numbers = {"2", "4", "6", "8", "10", "11", "13", "15", "17", "20", "22", "24", "26", "28", "29", "31",
                         "33", "35"}

        if self.bet_type == "number":
            self.win = (self.result == self.prediction)
        elif self.bet_type == "color":
            if self.result == "0":
                self.win = False
            else:
                if self.prediction.lower() == "red":
                    self.win = self.result in red_numbers
                elif self.prediction.lower() == "black":
                    self.win = self.result in black_numbers
        elif self.bet_type == "odd_even":
            if self.result == "0":
                self.win = False
            else:
                if self.prediction.lower() == "odd":
                    self.win = (int(self.result) % 2 == 1)
                elif self.prediction.lower() == "even":
                    self.win = (int(self.result) % 2 == 0)
        elif self.bet_type == "low_high":
            if self.result == "0":
                self.win = False
            else:
                if self.prediction.lower() == "low":
                    self.win = 1 <= int(self.result) <= 18
                elif self.prediction.lower() == "high":
                    self.win = 19 <= int(self.result) <= 36
        self.save()