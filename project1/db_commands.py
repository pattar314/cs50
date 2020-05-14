import os
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

def insert_book(isbn, author, title, date):
    newBook = {'isbn': isbn, 'author': author, 'title': title, 'date': date}
    db.execute(f'INSERT INTO books (isbn, author, title, date) VALUES ({ isbn }, {author}, {title}, {date})')

def import_db():
    bookshelf = db.execute("SELECT isbn, author, title, date, FROM books").fetchall()
    for book in bookshelf:
        print(f'Book {book.isbn} is {book.title} by {book.author} in {book.date}')

if __name__ == "__main__":
    import_db()