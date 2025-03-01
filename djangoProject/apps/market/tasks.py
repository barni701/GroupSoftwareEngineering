from celery import shared_task
from django.core.management import call_command

@shared_task
def update_stock_prices_task():
    call_command('update_stock_prices')

@shared_task
def generate_market_event_task():
    call_command('generate_market_events')