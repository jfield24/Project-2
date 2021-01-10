from flask import Flask, render_template, redirect, Response
from flask_pymongo import PyMongo
import run_api
import json
import requests
from config import api_key
import pandas as pd
import time
from datetime import datetime, date
from dateutil.relativedelta import relativedelta, MO

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/stock_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    stock = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html",stock=stock)


# # Route that will trigger the scrape function
@app.route("/api")
def api():

    stock = mongo.db.stock
    stock_data = run_api.run_info()
    stock.update({}, stock_data, upsert=True)
    #return "API successful!"
    return redirect("/")


@app.route("/articles")
def articles():

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

    data = articles_df.to_json()

    return render_template("index.html",data=data)      

@app.route("/",methods=['GET'])
def staticpython(filename):

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
