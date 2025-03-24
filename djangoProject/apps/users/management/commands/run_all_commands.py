from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs a series of custom management commands sequentially.'

    def handle(self, *args, **options):
        commands = [
            'generate_rewards',
            'load_buildings',
            'populate_policies',
            'load_recipies',
            'update_item_values',
            'load_buildings_farm',
            'seed_data',
        ]

        for command in commands:
            self.stdout.write(self.style.SUCCESS(f'Running command: {command}'))
            call_command(command)
            self.stdout.write(self.style.SUCCESS(f'Finished command: {command}\n'))