from django.apps import AppConfig


# Define the config for the home app
class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # Set the name of the app
    name = "home"
