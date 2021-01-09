import requests
from pprint import pprint
from config import api_key
import pandas as pd
import time
from datetime import datetime, date
from dateutil.relativedelta import relativedelta, MO


def run_nyt():
    
    articles_df = pd.read_csv('articles.csv')
    company = "Netflix" 
    # Search for articles that mention company name
    query = company

    articles_df["Articles"] = ''
    for index, row in articles_df.iterrows():
        try:
            query = company
            date = datetime.strptime(row['Date'], '%d/%m/%Y').date()
            begin_date = date.strftime('%Y%m%d')
            end_date = (date + relativedelta(years=+1)).strftime('%Y%m%d')
            url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key={api_key}&q={query}&begin_date={begin_date}&end_date={end_date}"
            #print(url)
            article = requests.get(url).json()
            time.sleep(2)
            articles_df.loc[index, "Articles"] = article['response']['meta']['hits']
            
        except KeyError:
            articles_df.loc[index, "Articles"] = 0

    article_data = {}
    article_data["Date"]: articles_df["Date"]
    article_data["Articles"]: articles_df["Articles"]

    # Return results
    return article_data    
    
