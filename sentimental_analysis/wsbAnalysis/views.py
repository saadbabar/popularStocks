from django.shortcuts import render
from .models import RedditPost
from .serializers import RedditPostSerializer
from rest_framework import viewsets, generics
from datetime import date
import requests
from django.http import JsonResponse
from .reddit import fetch_reddit_posts, fetch_fmp_company_tickers, fetch_company_tickers, get_todays_extractions, compare_td_with_top
from .data import fmp_key


# Create your views here.

# def reddit_post_list(request):
#     posts = RedditPost.objects.all()
#     return render(request, 'reddit_post_list.html', {'posts': posts})

class RedditPostViewSet(viewsets.ModelViewSet):
    queryset = RedditPost.objects.all()
    serializer_class = RedditPostSerializer

class TodayRedditPostList(generics.ListAPIView):
    serializer_class = RedditPostSerializer

    def get_queryset(self):
        today =  date.today()
        return RedditPost.objects.filter(created_at__date=today)

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
        result = compare_td_with_top(fmp_key, td_extractions)
        return JsonResponse(result)  # Return result as JSON
    else:
        return JsonResponse({"error": "No extractions found"})