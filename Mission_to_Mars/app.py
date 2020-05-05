from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/vacation_to_mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("/index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mongo.db.mars_data.drop()
    mars_data = mongo.db.mars_data
    mars_results = scrape_mars.scrape()
    mongo.db.mars_data.insert_one(mars_results)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
