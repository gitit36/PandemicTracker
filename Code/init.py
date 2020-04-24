# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
import hashlib
from Models.Database import Database

# Initialize the app from Flask
app = Flask(__name__)

Database = Database()


# Define a route to hello function
@app.route("/")
def hello():
    data = Database.searchCountry("Wow")
    print(data)

    return render_template("home.html", countries=data)


# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)

