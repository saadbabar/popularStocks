import praw
import re
from .models import RedditPost
import finnhub # Using this to get all company names with tickers

COMMON_SUFFIXES = [
    # can add more later
    'inc',
    'corp',
    'corporation',
    'ltd',
    'holdings',
    'group', 
    'plc',
    'co',
    'llc'
]
finnhub_client = finnhub.Client(api_key='cs625mhr01qv8tfqdffgcs625mhr01qv8tfqdfg0')

def clean_name(name):
    """
    take suffixes out of company name
    tesla, inc will become tesla
    """
    name = name.lower()
    for suffix in COMMON_SUFFIXES:
        name = re.sub(r'\b' + suffix + r'\b', '', name)

    return name.strip()


def fetch_company_tickers():
    "Returns a dictionary of company names to tickers"
    stocks = finnhub_client.stock_symbols('US') # Returns all US tickers
    company_tickers = {clean_name(stock['description']): stock['symbol'] for stock in stocks}

    return company_tickers


company_tickers=fetch_company_tickers()  # Dictionary [{'description': 'apple', 'symbol': 'AAPL'}]


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