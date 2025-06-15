from django.core.management.base import BaseCommand
from currency_rates.models import CurrencyRate
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Creates test data for currency rates'

    def handle(self, *args, **kwargs):
        currencies = ['USD', 'EUR', 'GBP']
        start_date = date(2024, 1, 1)
        end_date = date(2024, 12, 31)
        current_date = start_date

        while current_date <= end_date:
            for currency in currencies:
                rate = round(random.uniform(50, 100), 4)
                CurrencyRate.objects.create(
                    currency=currency,
                    rate=rate,
                    date=current_date
                )
            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Successfully created test data')) 