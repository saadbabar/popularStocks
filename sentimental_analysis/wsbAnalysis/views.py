from django.shortcuts import render
from .models import RedditPost

# Create your views here.

def reddit_post_list(request):
    posts = RedditPost.objects.all()
    return render(request, 'reddit_post_list.html', {'posts': posts})