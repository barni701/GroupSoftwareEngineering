from django.apps import AppConfig

class MarketConfig(AppConfig):
    name = 'apps.market'

    def ready(self):
        # This forces the tasks module to be imported and registered
        import apps.market.tasks