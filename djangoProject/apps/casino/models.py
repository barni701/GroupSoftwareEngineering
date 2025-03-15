from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
import random

from decimal import Decimal

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


class BlackjackGame(models.Model):
    RESULT_CHOICES = [
        ('in_progress', 'In Progress'),
        ('win', 'Win'),
        ('lose', 'Lose'),
        ('push', 'Push'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet_amount = models.DecimalField(max_digits=12, decimal_places=2)
    # We'll store the deck and hands as JSON lists of card strings.
    deck = models.JSONField(default=list)
    player_hand = models.JSONField(default=list)
    dealer_hand = models.JSONField(default=list)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='in_progress')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def initialize_game(self):
        """Initializes a new game: sets up a deck and deals two cards each to player and dealer."""
        self.deck = self.create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.result = 'in_progress'
        self.save()

    def card_value(self, card):
        """Returns the numeric value of a card string (e.g., 'K of Hearts' returns 10, 'A of Clubs' returns 11)."""
        rank = card.split()[0]
        if rank in ['J', 'Q', 'K']:
            return 10
        if rank == 'A':
            return 11  # Adjust for Ace later if needed
        return int(rank)
    
    def hand_value(self, hand):
        """Calculates the total value of a hand, adjusting for Aces."""
        total = 0
        aces = 0
        for card in hand:
            val = self.card_value(card)
            total += val
            if card.split()[0] == 'A':
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total
    
    def player_value(self):
        return self.hand_value(self.player_hand)
    
    def dealer_value(self):
        return self.hand_value(self.dealer_hand)
    
    def hit(self):
        """Deals one card to the player and checks for bust."""
        if self.deck:
            self.player_hand.append(self.deck.pop())
            self.save()
    
    def dealer_play(self):
        """Dealer hits until the hand value is at least 17."""
        while self.dealer_value() < 17 and self.deck:
            self.dealer_hand.append(self.deck.pop())
        self.save()
    
    def determine_result(self):
        """Determines and sets the result based on final hand values."""
        player_total = self.player_value()
        dealer_total = self.dealer_value()
        if player_total > 21:
            self.result = 'lose'
        elif dealer_total > 21 or player_total > dealer_total:
            self.result = 'win'
        elif player_total == dealer_total:
            self.result = 'push'
        else:
            self.result = 'lose'
        self.save()