import praw
import re
from .models import RedditPost
import finnhub # Using this to get all company names with tickers
import nltk
import requests
from nltk.corpus import stopwords # remove unneccary words from sentence like you
from .data import COMMON_SUFFIXES,COMMON_PREFIXES,  company_tickers_manual, words_to_avoid, fmp_key
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
nltk.download('stopwords')

stop_words=set(stopwords.words('english'))


finnhub_client = finnhub.Client(api_key='cs625mhr01qv8tfqdffgcs625mhr01qv8tfqdfg0')

def remove_stopwords(sentence):
    """
    Removes articles and other words like 'you' 'the' 'a' from sentence
    """
    words = sentence.split()
    filtered_words = [word for word in words if word.lower() not in stop_words] # take out stop words
    return ' '.join(filtered_words)

def filtered_sentence(sentence):
    filter1 = remove_stopwords(sentence)

    filter1 = filter1.replace("'s", "")
    filter1 = filter1.replace("’s", "")
    filter1 = filter1.replace(",", "")
    filter1 = filter1.replace(".", "")

    return filter1


def clean_name(name):
    """
    take suffixes out of company name
    tesla, inc will become tesla
    This function is to clean up finnhub data
    """
    if name is None:
        return 'unknown'
    name = name.lower()

    # Remove common prefixes
    for prefix in COMMON_PREFIXES:
        name = re.sub(r'^' + re.escape(prefix) + r'\s+', '', name)  # Match prefix at the start

    for suffix in COMMON_SUFFIXES:
        name = re.sub(r'\b' + re.escape(suffix) + r'[\.,]*\b', '', name)

    name = re.sub(r'[.,\s]+$', '', name)

    # Remove multiple spaces and trim the name
    name = re.sub(r'\s+', ' ', name).strip()

    return name


def fetch_company_tickers():
    "Returns a dictionary of company names to tickers -- finnhub"
    stocks = finnhub_client.stock_symbols('US') # Returns all US tickers in stocks = {stock1{...}, stock2{...}} format
    company_tickers = {clean_name(stock['description']): stock['symbol'] for stock in stocks}

    return company_tickers

def fetch_fmp_company_tickers(api_key):
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}"

    response = requests.get(url)
    if response.status_code ==200:
        all_companies = response.json()
        cmp_tickers = {clean_name(stock['name']): stock['symbol'] 
                       for stock in all_companies 
                       if (stock.get('exchangeShortName') in ['NYSE', 'NASDAQ']) 
                       and (stock.get('type') == 'stock')}
        # for stock in all_companies:
        #     if 'TSLA' in stock.values():
        #         print(f"Original: {stock['name']}, Cleaned: {clean_name(stock['name'])}")

        return cmp_tickers
    else:
        print(f"error getting data from endpoint: {response.status_code}")
        return None


company_tickers=fetch_company_tickers()  # Dictionary [{'apple','AAPL'}] for finnhub call
fmp_company_tickers = fetch_fmp_company_tickers(fmp_key) # for fmp call


def extract_stock_symbol(string, company_tickers, fmp_company_tickers):
    "Takes string and parses for stock ticker"
    words = string.split()

    for word in words:
        if len(word) < 2:
            continue
        if word[0] == "$":
            return word[1:]  # returns ticker without $

        if word in words_to_avoid:
            continue

        # commented out finnhub api call for now
        
        if word.lower() in company_tickers:
            return company_tickers[word.lower()] # this case checks in finnhub
        
        if word.upper() in company_tickers.values():
            return word.upper() # handles case where someone says aapl or AAPL, also checks in finnhubb
        
        if word.lower() in fmp_company_tickers:
            return fmp_company_tickers[word.lower()] # this case and next case check data.py
        
        if word.upper() in fmp_company_tickers.values():
            return word.upper()
        
        

    return None


def get_todays_extractions():
    "returns today's hot posts also cleans the response by only giving us sentiment score and ticker"
    url = 'http://localhost:8000/posts/today/'
    response = requests.get(url)

    if response.status_code == 200:
        reddit_data = response.json()
        cleaned_data = {stock['stock_mentioned']: stock['sentiment_score'] for stock in reddit_data}
        return cleaned_data
    else:
        print(f"Failed to get data: {response.status_code}")
        return None

def compare_td_with_top(api_key, stock_data):
    "This function takes the get_todays_extraction function ann makes sure that the companies are top movers"
    url = f"https://financialmodelingprep.com/api/v3/stock_market/actives?apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        top_movers = response.json()
        extracted_movers = {stock['symbol'] for stock in top_movers}

        filter_daily_movers = {stock: score for stock, score in stock_data.items() if stock in extracted_movers}
        return filter_daily_movers 
    else:
        print(f"failed to fulfill task: {response.status_code}")
        return None

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

def combine_duplicates(dictionary: dict[str, float]) -> dict[str, float]:
    my_dict: dict[str, float] = {}
    count_dict: dict[str, int] = {}  

    for key, value in dictionary.items():
        if key in my_dict:
            # Update the total value and the count
            my_dict[key] += value
            count_dict[key] += 1
        else:
            # Initialize the key with its first occurrence
            my_dict[key] = value
            count_dict[key] = 1

    # Calculate the average for each key
    for key in my_dict:
        my_dict[key] /= count_dict[key]

    return my_dict
        
def fetch_reddit_posts(company_tickers, fmp_company_tickers):
    reddit = praw.Reddit (
        client_id = '7hzi_mwWJPDsizSxbZvSAg',
        client_secret = 'cduDvCKuWtewpRO8mUu0mDylbMLTOw',
        user_agent = 'WallStreetBetsSentiment:v1.0 (by Saad Babar)'
    )

    subreddit = reddit.subreddit('wallstreetbets')
    for submission in subreddit.hot(limit=12):
        stock = extract_stock_symbol(filtered_sentence(submission.title), company_tickers, fmp_company_tickers)
        if stock == None:
            continue
        sentiment_score = analyze_sentiment(submission.title + submission.selftext)

        if RedditPost.objects.filter(post_id=submission.id).exists():
            continue

        # If post already exists, then skip
        RedditPost.objects.get_or_create(
            post_id=submission.id,
            title = submission.title,
            body=submission.selftext,
            sentiment_score=sentiment_score,
            stock_mentioned=stock
        )

if __name__ == "__main__":
    get_todays_extractions()