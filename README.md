# WallStreetBets NLP Sentiment Analyzer
This Program extracts latest data from the wallstreetbets subreddit and performs sentimental analysis to return which stocks are popular at the moment.

For this program, I performed multiple full-stack related tasks like:
- Using external API endpoints for data that can be used within my program(Reddit's API and Python PRAW library, and Financial Modeling Prep API endpoints to get specific data for symbols and company names within US markets (NYSE and NASDAQ))

- Created multiple modules/functions to clean incoming raw JSON data that can later be used with the program

    - For example i created multiple functions to clean names of the companies. For example most people on Reddit won't say "The Boeing Company" or "Rivian Automotive, Inc", they'll say things like "Boeing" or "Rivian", respectively.
    
    - Also i created functions to parse out punctuation from names, as well "'s" because the goal is to reach as many way people can say something and strip everything so that only the name is left. This is important because people can say something multiple different ways since we are extracting what they are saying from the title of a reddit post

- I created unit tests for the functions as well as Python Scripts to ensure function performance and reliability.

- Used NLP libraries like VADER to perform sentiment analysis on reddit titles and text bodies to see what is the general outlook of a particular stock

- Created SQL schema in Django framework and linked it to database in PostgreSQL

- I developed REST API endpoints using the Django REST Framework to get all the data that has been fetched so far and the data that is specific to a day(necessary for frontend where the data for the day will passed for visualization in the dashboard)

- I also strengthened version control skills in this project

- so basically we pass in the request into typescipt where the data of today lies and we pass it into a await/fetch request and then typescript will take that data and make into a graph

- Note to Self: Both the django server (in sentimental_analysis) (python3 manage.py runserver) and in the stock-sentiment-dashboard (npm run start) must be active for it to run

Final Data to be processed by frontend:
![Local Image](./exampleredirect.png)

Data Visuals processed by frontend:
![Local Image](./exampleoutput.png)



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
