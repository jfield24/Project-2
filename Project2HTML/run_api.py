import requests
from config import api_key
import time




def run_info():
   
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    company = "Netflix"

    
    # Search for articles that mention company name
    query = company

    # Build query URL
    query_url = url +"q=" + query + "&fq=news_desk:(Business)&page=0&sort=newest&api-key=" + api_key

    # Request articles
    articles = requests.get(query_url).json()
    time.sleep(2)
    
   # The "response" property in articles contains the actual articles
   # list comprehension.
    articles_list = articles["response"]["docs"]

    # Store top 5 articles urls and names
    web_urls = []
    for article in articles_list[:5]:
        web_urls.append("https://www.nytimes.com/" + article["multimedia"][0]["url"])
    article_names = []

    for article in articles_list[:5]:
        article_names.append(article["headline"]["main"])

    article_image_urls = []
    for x in range(len(web_urls)):
        article_image_urls.append({'title':article_names[x], 'img_url': web_urls[x]})

    #Find feature article and its features
    feature_article = articles_list[0]

    feature_article_url = feature_article["web_url"]
    feature_article_name = feature_article["headline"]["main"]
    feature_image_link = "https://www.nytimes.com/" + feature_article["multimedia"][0]["url"]
    feature_article_lead = feature_article["lead_paragraph"]
    
     # Creating the dictionary to hold all the API data
    stock_data = {}
    stock_data ["feature_title"]: feature_article_name
    stock_data[ "feature_p"]: feature_article_lead
    stock_data["feature_link"]: feature_article_url
    stock_data["featured_image_url"]: feature_image_link
    stock_data["article_image_urls"]: article_image_urls

    # Return results
    return stock_data
