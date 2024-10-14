from django.core.management.base import BaseCommand
from wsbAnalysis.reddit import fetch_fmp_company_tickers
from wsbAnalysis.data import fmp_key
import json

class Command(BaseCommand):
    help = 'should return what the endpoint for fmp is supposed to'
    
    def handle(self, *args, **kwargs):
        result = fetch_fmp_company_tickers(fmp_key)
        if result:
            # Convert the dictionary to a JSON string for better readability
            self.stdout.write(json.dumps(result, indent=4))
        else:
            self.stdout.write("Failed to fetch data from FMP API")