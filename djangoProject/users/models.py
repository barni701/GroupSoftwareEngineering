from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gdpr_consent = models.BooleanField(default=False)
    consent_date = models.DateTimeField(auto_now_add=True)
    #two_factor_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"