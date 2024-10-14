# WallStreetBets NLP Sentiment Analyzer
This Program extracts latest data from the wallstreetbets subreddit and performs sentimental analysis to return which stocks are popular at the moment.
For this program, I performed multiple full-stack related tasks like:
- Using external API endpoints for data that can be used within my program(Reddit's API and Python PRAW library, and Finanial Modeling Prep API endpoints to get specific data for symbols and company names within US markets (NYSE and NASDAQ))
- Created multiple modules/functions to clean incoming raw JSON data that can later be used with the program
    - For example i created multiple functions to clean names of the companies. For example most people on Reddit won't say "The Boeing Company" or "Rivian Automotive, Inc", they'll say things like "Boeing" or "Rivian", respectively.
- I created unit tests for the functions as well as Python Scripts to ensure function performance and reliability.
- I developed REST API endpoints using the Django REST Framework to get all the data that has been fetched so far and the data that is specific to a day(necessary for frontend where the data for the day will passed for visualization in the dashboard)
- I also strengthened version control skills in this project
- More to come

# Goals:
- Python
- TypeScript
- d3.js
- APIs
- Version Control
- Django
- REST APIs
- Natural Language Processing
- Celery Task Automater
- Webscraping with Pandas


# APIs used: 
- Reddit API
- Finnhub API
- Financial Modeling Prep API (using this over finnhub because of better data)
