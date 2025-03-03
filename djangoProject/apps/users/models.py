from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tc_consent = models.BooleanField(default=False)
    consent_date = models.DateTimeField(auto_now_add=True)

    # Existing currency
    currency_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    # New currency (farm-generated)
    farm_currency = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Methods for regular currency (unchanged)
    def add_currency(self, amount, description="Credit added"):
        from django.db import transaction
        amount = Decimal(amount)
        with transaction.atomic():
            self.currency_balance += amount
            self.save()
            CurrencyTransaction.objects.create(
                profile=self,
                transaction_type='credit',
                amount=amount,
                description=description
            )

    def deduct_currency(self, amount, description="Debit applied"):
        from django.db import transaction
        amount = Decimal(amount)
        with transaction.atomic():
            if self.currency_balance >= amount:
                self.currency_balance -= amount
                self.save()
                CurrencyTransaction.objects.create(
                    profile=self,
                    transaction_type='debit',
                    amount=amount,
                    description=description
                )
                return True
            return False

    # Methods for new farm currency
    def add_farm_currency(self, amount, description="FarmCoin added"):
        """Add the new farm currency to the user's balance."""
        from django.db import transaction
        amount = Decimal(amount)
        with transaction.atomic():
            self.farm_currency += amount
            self.save()
            FarmCurrencyTransaction.objects.create(
                profile=self,
                transaction_type='credit',
                amount=amount,
                description=description
            )

    def deduct_farm_currency(self, amount, description="FarmCoin spent"):
        """Deduct the farm currency for purchases."""
        from django.db import transaction
        amount = Decimal(amount)
        with transaction.atomic():
            if self.farm_currency >= amount:
                self.farm_currency -= amount
                self.save()
                FarmCurrencyTransaction.objects.create(
                    profile=self,
                    transaction_type='debit',
                    amount=amount,
                    description=description
                )
                return True
            return False

    def calculate_green_impact(self):
        # Sum over each investment: sustainability_rating * shares
        total = Decimal('0.00')
        for investment in self.user.investments.all():
            total += investment.company.sustainability_rating * investment.shares
        return total

class CurrencyTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
         ('credit', 'Credit'),
         ('debit', 'Debit'),
    )
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.profile.user.username} {self.transaction_type} {self.amount} on {self.created_at}"

class FarmCurrencyTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="farm_transactions")
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username} {self.transaction_type} {self.amount} on {self.created_at}"