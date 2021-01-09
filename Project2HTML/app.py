from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import run_api
import run_article

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
    return "API successful!"
    #return redirect("/")


@app.route("/articles")
def articles():

    stock = mongo.db.stock
    article_data = run_article.run_nyt()
    stock.update({}, article_data, upsert=True)
    return "API successful!"
    #return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
