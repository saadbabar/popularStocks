from django.shortcuts import render
from .models import RedditPost
from .serializers import RedditPostSerializer
from rest_framework import viewsets, generics
from datetime import date


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
