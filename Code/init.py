# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
import hashlib
from Models.Database import Database
from Models.CountryList import CountryList

# Initialize the app from Flask
app = Flask(__name__)

Database = Database()
CountryList = CountryList()


# Define a route to hello function
@app.route("/")
def hello():
    Database.updateAll()
    data = Database.viewCountry()
    print(data)
    return render_template("home.html", countries=data)


@app.route("/<string:theName>")
def ownCountry(theName):
    x = theName
    data = Database.searchCountry(x)
    print(data)
    return render_template("singleCountry.html", countries=data)


# Define a route to country function
@app.route("/country")  # , methods=["GET","POST"]'''
def countrystat():
    data = Database.viewCountry()
    print(data)
    return render_template("country.html", countries=data)


# Define a route to Compare Countries
@app.route("/compare_countries")
def countrycompare():
    data = Database.viewCountry()
    print(data)
    return render_template("compare_countries.html", countries=data)


@app.route("/health_guidelines")
def getGuidlines():
    return render_template("health.html")


# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
