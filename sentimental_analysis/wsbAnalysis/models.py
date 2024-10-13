from django.db import models

# Create your models here.
class RedditPost(models.Model):
    post_id = models.CharField(max_length=200, unique = True)
    title = models.TextField()
    body = models.TextField ()
    sentiment_score = models.FloatField()
    stock_mentioned = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title # Returns title of the post