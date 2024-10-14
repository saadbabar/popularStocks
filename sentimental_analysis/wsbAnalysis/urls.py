from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RedditPostViewSet, TodayRedditPostList, get_stock_sentiment
from . import views

# urlpatterns = [
#     path('posts/', views.reddit_post_list, name='reddit_post_list'),
# ]

router =  DefaultRouter()
router.register(r'posts', RedditPostViewSet)

urlpatterns = [
    path('posts/today/', TodayRedditPostList.as_view(), name='today-reddit-posts'),
    path('api/stock-sentiment/', get_stock_sentiment, name='stock-sentiment'),
    path('', include(router.urls)),
]
