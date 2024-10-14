import praw
import re
from .models import RedditPost
import finnhub # Using this to get all company names with tickers
import pandas as pd
import nltk
from nltk.corpus import stopwords # remove unneccary words from sentence like you
from .data import COMMON_SUFFIXES, company_tickers_manual, words_to_avoid
nltk.download('stopwords')

stop_words=set(stopwords.words('english'))


url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_list = pd.read_html(url)[0] # get first table in html

def manual_web_search(company_name, company_list):
    "This check is for when finnhub cannot find ticker"
    matches = company_list[company_list['Security'].str.contains(company_name, case=False)]
    if not matches.empty:
        return matches[[ 'Symbol']]
    else:
        None

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
    name = name.lower()
    for suffix in COMMON_SUFFIXES:
        name = re.sub(r'\b' + suffix + r'\b', '', name)

    return name.strip()


def fetch_company_tickers():
    "Returns a dictionary of company names to tickers -- finnhub"
    stocks = finnhub_client.stock_symbols('US') # Returns all US tickers in stocks = {stock1{...}, stock2{...}} format
    company_tickers = {clean_name(stock['description']): stock['symbol'] for stock in stocks}

    return company_tickers


company_tickers=fetch_company_tickers()  # Dictionary [{'apple','AAPL'}]


def extract_stock_symbol(string):
    "Takes string and parses for stock ticker"
    words = string.split()

    for word in words:
        if len(word) < 2:
            continue
        if word[0] == "$":
            return word[1:]  # returns ticker without $

        if word in words_to_avoid:
            continue
        
        if word.lower() in company_tickers:
            return company_tickers[word.lower()] # this case checks in finnhub
        
        if word.upper() in company_tickers.values():
            return word.upper() # handles case where someone says aapl or AAPL, also checks in finnhubb
        
        if word.lower() in company_tickers_manual:
            return company_tickers_manual[word.lower()] # this case and next case check data.py
        
        if word in company_tickers_manual.values():
            return company_tickers_manual(word)
        
        result_df = manual_web_search(word, sp500_list)  # Call the function again
        if result_df is not None and not result_df.empty:  # Check if the DataFrame is not empty
            return result_df['Symbol'].values[0]

    return None
        
        
def fetch_reddit_posts():
    reddit = praw.Reddit (
        client_id = '7hzi_mwWJPDsizSxbZvSAg',
        client_secret = 'cduDvCKuWtewpRO8mUu0mDylbMLTOw',
        user_agent = 'WallStreetBetsSentiment:v1.0 (by Saad Babar)'
    )

    subreddit = reddit.subreddit('wallstreetbets')
    for submission in subreddit.hot(limit=12):
        print(filtered_sentence(submission.title))
        stock = extract_stock_symbol(filtered_sentence(submission.title))
        print(stock)