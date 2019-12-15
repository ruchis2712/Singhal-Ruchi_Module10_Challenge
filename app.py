# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 13:33:16 2019

@author: rusinghal
"""


# Import dependencies for FLASK
from flask import Flask, render_template
from flask_pymongo import PyMongo

# to import a .py file from another location
import sys
sys.path.append('C:/Users/rusinghal/Desktop/DTPersonal/Post May 2016 Encryption/Berkley Extension Bootcamp docs/Class Work/Web Scraping/Singhal-Ruchi_Module10_Challenge')

import webscraper

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    print ("rendering page")
    mars = mongo.db.mars.find_one()
    print(mars)
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = webscraper.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run(debug=True)