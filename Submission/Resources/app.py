from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from scraping import ScraperHelper

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
   mars_data = mongo.db.mars_info.find_one()
   return render_template("index.html", mars=mars_data)

@app.route("/scrape")
   
def scrape():
   scraper = ScraperHelper
   mars_data = scraper.scrape_all()
   mars_info= mongo.db.mars_info
   mars_info.update_one({}, {"$set": mars_data}, upsert=True)
   return redirect("/")
# code=302

if __name__ == "__main__":
   app.run(debug=True)
