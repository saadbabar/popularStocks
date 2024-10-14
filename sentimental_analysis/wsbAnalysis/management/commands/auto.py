"Automated script to pass data to front end"
from django.core.management.base import BaseCommand
from wsbAnalysis.reddit import fetch_reddit_posts, fetch_fmp_company_tickers, fetch_company_tickers, get_todays_extractions, compare_td_with_top 
from wsbAnalysis.data import fmp_key

class Command(BaseCommand):
    help = "run this script on celery to automate frontend updates"

    def handle(self, *args, **kwargs):
        company_tickers = fetch_company_tickers()
        fmp_company_tickers = fetch_fmp_company_tickers(fmp_key)
        fetch_reddit_posts(company_tickers, fmp_company_tickers)
        td_extractions = get_todays_extractions()
        if td_extractions:
            # Compare today's extractions with top movers
            result = compare_td_with_top(fmp_key, td_extractions)
            
            # Convert the dictionary to a formatted string and output it
            self.stdout.write(str(result))
        else:
            self.stdout.write("No extractions found.")



