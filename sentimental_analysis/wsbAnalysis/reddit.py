import praw
from .models import RedditPost
import finnhub # Using this to get all company names with tickers


finnhub_client = finnhub.Client(api_key='cs625mhr01qv8tfqdffgcs625mhr01qv8tfqdfg0')

def fetch_company_tickers():
    "Returns a dictionary of company names to tickers"
    stocks = finnhub_client.stock_symbols('US') # Returns all US tickers
    company_tickers = {stock['description'].lower(): stock['symbol'] for stock in stocks}

    return company_tickers

company_tickers=fetch_company_tickers()


def extract_stock_symbol(string):
    "Takes string and parses for stock ticker"
    for word in string:
        if word[0] == "$":
            return word[1:]  # returns ticker without $
        
        
def fetch_reddit_posts():
    reddit = praw.Reddit (
        client_id = '7hzi_mwWJPDsizSxbZvSAg',
        client_secret = 'cduDvCKuWtewpRO8mUu0mDylbMLTOw',
        user_agent = 'WallStreetBetsSentiment:v1.0 (by Saad Babar)'
    )

    subreddit = reddit.subreddit('wallstreetbets')
    for submission in subreddit.hot(limit=10):
        print(submission.title)