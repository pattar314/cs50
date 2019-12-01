import os
import requests

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

active_login_token = False

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app.debug = 1
app.DATABASE_URL='postgres://ctiazebqyiyhlf:349007f1e4d3c17da2a3c149efb9ef17e521f4a38c2c0c570968c4e5735cefb1@ec2-174-129-210-249.compute-1.amazonaws.com:5432/daj1jc00ojlhg6'

def main():
    flights = db.execute('SELECT origin, destination, duration FROM flights').fetchAll()

@app.route("/")
def index():
    try:
        return render_template('index.html')
        #if active_login_token == False:
        #    return render_template('login-register.html')
        
    except Exception as err:
        print(repr(err))
        return render_template('error.html', err = repr(err))
    

@app.route('/register')
def register():
    try:
        return "This is the registration page"
    except Exception as err:
        print(repr(err))
        return render_template('error.html')
    

@app.route("/login")
def login():
    try:
        return 'This is the login page'
    except Exception as err:
        print(repr(err))
        return render_template('error.html')
    

@app.route("/import")
def import_data():
    try:
        return 'this is where you will be importing data'
    except Exception as err:
        print(repr(err))
        return render_template('error.html')
    


@app.route("/book_page")
def buildBookPage():
        try:
            return 'coming soon'
        except Exception as err:
            print(repr(err))
            return render_template('error.html')
    

@app.route("/submit_review")
def submit_review():
        try:
            return 'submit comming soon'
        except Exception as err:
            print(repr(err))
            return render_template('error.html')
    

@app.route("/review_data")
def review_data():
        try:
            return 'this is the data review'
        except Exception as err:
            print(repr(err))
            return render_template('error.html')
    

@app.route('/api/<int:isbn>')
def api_direct(isbn):
        try:
            return f'this is api direct for isbn { isbn }'
        except Exception as err:
            print(repr(err))
            return render_template('error.html')
        

@app.route('/error')
def return_error():    
    try:
        return render_template('error.html')
    except Exception as err:
        print(repr(err))
        
    return 'you have encountered an error'



''' ------------------------------------------------------
    TODO: 1.check for cookie
          2a. if cookie is not found assume this to be the first visit and direct to login/register
          2b. if cookie is found check to see if it is valid and if so direct to user landing page

          register
          1. check to see if user exists
          2a. if user does not exist. create user and assign encrypted form of password to that user
              and store as a cookie
          2b. if user does exist check for a history
          3a. if there is no history prep to add an entry in the history and send request for an
              entry from the database



   '''