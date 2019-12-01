
import os
import sys
import csv
import requests

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

if __name__ == '__main__':
    # todo check to see if the db and table exist. If not add the database and then
    # create a table and then add an updated 

    with open('books.csv', newline='') as book_file:
        books = book_file.readlines()
        for book in books:
            book = book.split(',')
            isbn = book[0]
            title = book[1]
            author = book[2]
            publish_date = book[3]
            print(f'Congratulations you have added {title} by {author}')
    
    '''flights = db.execute("SELECT id, origin, destination, duration, FROM flights ").fetchall()
    for flight in flights:
        print(f'Flight {flight.id}: {flight.origin} to {flight.destination}, {flight.duration} minutes')
    '''
