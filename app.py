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

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/users")
def users():
    return render_template('users.html')

@app.route("/devices")
def devices():
    return render_template('devices.html')

@app.route("/add-device")
def add_device():
    return render_template('addDevice.html')
if __name__ == "__main__":
    app.run(debug=True)

import admin
