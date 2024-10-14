from django.core.management.base import BaseCommand
from wsbAnalysis.reddit import fetch_reddit_posts

class Command(BaseCommand):
    help = 'Fetch the 10 recent hottest posts in wsb subreddit'

    def handle(self, *args, **kwargs):
        fetch_reddit_posts()
        self.stdout.write(self.style.SUCCESS('Successfully fetched'))