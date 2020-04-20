
import os
import sys
import csv
import requests
import re

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


def insert_book(isbn, title, author, date):
    try:
        db.execute(f'INSERT INTO books VALUES (:isbn, :title, :author, :date)', { 'isbn': isbn, 'title': title , 'author': author , 'date': date })
    except Exception as err:
        print(f'an error has occured \n { repr(err) } \n\n')
        exit()
    finally:
        print(f'isbn: {isbn}, title: {title}, author: {author}, date: {date}')
        print('operation done')

if __name__ == '__main__':
    # todo check to see if the db and table exist. If not add the database and then
    # create a table and then add an updated
    # 
    with open('books.csv') as book_file:
        reader = csv.reader(book_file)
        for isbn, title, author, date in reader:
            insert_book(isbn, title, author, date)
            print(f'Congratulations you have added {title} by {author}\n\n\n')
        
        db.commit()
        print('all finished')



# db.execute('CREATE TABLE books ( isbn VARCHAR NOT NULL UNIQUE, title VARCHAR NOT NULL, author VARCHAR, date INT)')