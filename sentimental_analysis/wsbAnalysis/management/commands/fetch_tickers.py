from django.core.management.base import BaseCommand
from wsbAnalysis.reddit import fetch_company_tickers

class Command(BaseCommand):
    help = 'Should return dictionary of all US tickers'

    def handle(self, *args, **kwargs):
       dictionary = fetch_company_tickers()

       self.stdout.write(self.style.SUCCESS(f'Dictionary {dictionary}'))