from __main__ import app
from flask import Flask, render_template, request, session, redirect
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from dbconnection import connection
from datetime import datetime
# from flask_mail import Mail
import os
import json
import math
from dbconnection import connection

