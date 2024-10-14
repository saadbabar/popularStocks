from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RedditPostViewSet, TodayRedditPostList
from . import views

# urlpatterns = [
#     path('posts/', views.reddit_post_list, name='reddit_post_list'),
# ]

router =  DefaultRouter()
router.register(r'posts', RedditPostViewSet)

urlpatterns = [
    path('posts/today/', TodayRedditPostList.as_view(), name='today-reddit-posts'),
    path('', include(router.urls)),
]
