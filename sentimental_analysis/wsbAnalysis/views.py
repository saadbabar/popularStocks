from django.shortcuts import render
from .models import RedditPost
from .serializers import RedditPostSerializer
from rest_framework import viewsets, generics
from datetime import date
import requests
from django.http import JsonResponse
from .reddit import fetch_reddit_posts, fetch_fmp_company_tickers, fetch_company_tickers, get_todays_extractions, compare_td_with_top, combine_duplicates
from .data import fmp_key
from django.utils import timezone
import pytz
from datetime import timedelta
import logging


# Create your views here.

# def reddit_post_list(request):
#     posts = RedditPost.objects.all()
#     return render(request, 'reddit_post_list.html', {'posts': posts})

class RedditPostViewSet(viewsets.ModelViewSet):
    queryset = RedditPost.objects.all()
    serializer_class = RedditPostSerializer


logger = logging.getLogger(__name__)

class TodayRedditPostList(generics.ListAPIView):
    serializer_class = RedditPostSerializer

    def get_queryset(self):
        # Define the user's local time zone
        user_timezone = pytz.timezone('America/New_York')  # Eastern Time Zone

        # Get the current time in the user's local time zone
        now_local = timezone.now().astimezone(user_timezone)

        # Start and end of the day in the user's local time zone
        start_of_day_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day_local = start_of_day_local + timedelta(days=1)

        # Convert the start and end times back to UTC for filtering
        start_of_day_utc = start_of_day_local.astimezone(pytz.utc)
        end_of_day_utc = end_of_day_local.astimezone(pytz.utc)

        # Log times for debugging
        logger.info(f"Server current time (UTC): {timezone.now()}")
        logger.info(f"Local time now ({user_timezone}): {now_local}")
        logger.info(f"Filtering posts from {start_of_day_local} to {end_of_day_local} in local time")
        logger.info(f"Corresponding UTC range from {start_of_day_utc} to {end_of_day_utc}")

        # Filter RedditPost created within today's date in user's local time zone
        queryset = RedditPost.objects.filter(created_at__range=(start_of_day_utc, end_of_day_utc))

        logger.info(f"Number of posts found: {queryset.count()}")
        return queryset

def get_stock_sentiment(requests):
    # Fetch the necessary data
    company_tickers = fetch_company_tickers()
    fmp_company_tickers = fetch_fmp_company_tickers(fmp_key)
    
    # Run the Reddit post extraction
    fetch_reddit_posts(company_tickers, fmp_company_tickers)
    
    # Get today's stock mentions and sentiment
    td_extractions = get_todays_extractions()
    
    if td_extractions:
        # Compare with top movers
        combined_sentiment = combine_duplicates(td_extractions)
        result = compare_td_with_top(fmp_key, combined_sentiment)
        return JsonResponse(result)  # Return result as JSON
    else:
        return JsonResponse({"error": "No extractions found"})