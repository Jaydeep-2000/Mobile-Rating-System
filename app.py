from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename
from dbconnection import connection
from datetime import datetime
# from flask_mail import Mail
import os
import json
import math



app = Flask(__name__, template_folder='templates')




@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/gadget")
def gadget():
    return render_template('gadget.html')


@app.route("/login")
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)

