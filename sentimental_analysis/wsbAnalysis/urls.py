from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.reddit_post_list, name='reddit_post_list'),
]