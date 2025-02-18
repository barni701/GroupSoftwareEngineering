from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    gdpr_consent = forms.BooleanField(
        required=True,
        label="I agree to the processing of my personal data in accordance with the GDPR.",
        help_text="You must agree to our terms to create an account."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gdpr_consent')