from django.core.management.base import BaseCommand
from wsbAnalysis.reddit import fetch_reddit_posts, fetch_fmp_company_tickers, fetch_company_tickers
from wsbAnalysis.data import fmp_key

class Command(BaseCommand):
    help = 'Fetch the 10 recent hottest posts in wsb subreddit'

    def handle(self, *args, **kwargs):
        company_tickers = fetch_company_tickers()
        fmp_company_tickers = fetch_fmp_company_tickers(fmp_key)
        fetch_reddit_posts(company_tickers, fmp_company_tickers)
        self.stdout.write(self.style.SUCCESS('Successfully fetched'))