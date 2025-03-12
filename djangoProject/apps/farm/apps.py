# apps/farm/apps.py
from django.apps import AppConfig


class FarmConfig(AppConfig):
    name = 'apps.farm'

    def ready(self):
        import apps.farm.signals