from rest_framework import serializers
from .models import RedditPost

# serilizer are fro converting model instances to JSON
class RedditPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditPost
        fields = ['post_id', 'title', 'body', 'sentiment_score', 'stock_mentioned', 'created_at']