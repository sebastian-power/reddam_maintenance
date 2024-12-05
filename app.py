from flask import Flask, redirect, render_template
import os
import mysql.connector

app = Flask(__name__)
app.config.from_object('config.DevConfig')

db = mysql.connector.connect(host="localhost", user="root", password=os.getenv("DB_PWD"))

@app.route("/")
def home_page():
    """Page looks different for everyone, redirects user to login/signup if cookies don't exist or are validated
    """
    return redirect("/login")

@app.route('/login')
def login():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)