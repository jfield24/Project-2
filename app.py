from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import run_api

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/stock_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", vacation=destination_data)


# Route that will trigger the scrape function
@app.route("/api")
def api():

    # Run the scrape function
    stock_data = run_api.run_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, stock_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
