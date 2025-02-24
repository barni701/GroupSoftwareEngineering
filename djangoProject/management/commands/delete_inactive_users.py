from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Delete inactive users after 1 year of inactivity'

    def handle(self, *args, **kwargs):
        one_year_ago = now() - timedelta(days=365)
        users_deleted, _ = User.objects.filter(last_login__lt=one_year_ago).delete()
        self.stdout.write(f"Deleted {users_deleted} inactive users")