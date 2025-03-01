from django import forms
from .models import Investment

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['shares']

class SellInvestmentForm(forms.Form):
    shares = forms.IntegerField(min_value=1, label="Shares to Sell")