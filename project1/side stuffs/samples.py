import os, requests, json

from flask import Flask, session, render_template, g, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

active_login_token = False

app = Flask(__name__)
db = SQLAlchemy()

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['FLASK_APP'] = 'application.py'
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



'''

<work>
  <id type="integer">19106895</id>
  <books_count type="integer">13</books_count>
  <ratings_count type="integer">10250</ratings_count>
  <text_reviews_count type="integer">820</text_reviews_count>
  <original_publication_year type="integer">2012</original_publication_year>
  <original_publication_month type="integer">7</original_publication_month>
  <original_publication_day type="integer">19</original_publication_day>
  <average_rating>3.96</average_rating>
  <best_book type="Book">
    <id type="integer">15808659</id>
    <title>Kill Decision</title>
    <author>
      <id type="integer">1956402</id>
      <name>Daniel Suarez</name>
    </author>
    <image_url>https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1365395383l/15808659._SY160_.jpg</image_url>
    <small_image_url>https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1365395383l/15808659._SY75_.jpg</small_image_url>
  </best_book>
</work>

===============================================================================================================

target[1][6] is the work folder

target[1][6][8] is the individual books

target[1][6][8][2] is the author list and the name is listed under name


for t in test:
    for x in list(t[8]):
        title = x[1].text
        author = x[2][1].text
        image_link = x[3].text
        isbn =  x[0].text
        book_object = { 'title' : title, 'author' : author, 'image_link': image_link, 'isbn': isbn }
        print(list(book_object))


for t in test:
...     for x in t[8]:
...             if x.tag == 'author':
...                     print(x[1].text)
...             else:
...                     print(x.tag, x.text)
... 


Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
AttributeError: '_elementtree._element_iterator' object has no attribute 'text'
for t in target[1][6]:
    for x in t[8]:
 
  File "<stdin>", line 3
    
    ^
IndentationError: expected an indented block
>>> new = target[1][6]
>>> 






for t in test:
    for x in t[8]:
        print(x[1].text)
        print(x[2][1].text)
        print(x[3].text)
        print(x[0].text)
        # book_object = { 'title' : title, 'author' : author, 'image_link': image_link, 'isbn': isbn }
        # print(list(book_object))




book_list = {}
for t in test:
    book_object = {}
    for x in list(t[8]):
        if x.tag == 'author':
            book_object['author'] = x[1].text
        
        else:
            book_object[x.tag] = x.text
    
    book_list[book_object['id']] = book_object
    print(f'this book is {book_object["title"]} by {book_object["author"]}\n\n')

for book in book_list:
    print(book)

'''

book_card = '''
<div id='card_container'>
  <img id='book-cover' alt='book cover for {% title %} by {% author %}' src={% book_card[imgId] %}>
  <div id='author-name'>{% book_card[author] %}</div>
  <div id='book-title'>{% book_card[title] %}</div>
</div>





class book_card = {
    def __init__(self, imgId, author, title, link):
        self.image = imgId,
        self.author = author,
        self.title = title,
        self.link = link
}

book_cards = []
# parse through search results and turn each book into a book card to be displayed
for result in results:
    book_cards.append(new book_card(result.image_url, result.author, result.title))







try:
     print(db.execute('SELECT * FROM books WHERE title LIKE %stardust% OR author LIKE %stardust% OR isbn LIKE %stardust%'))
except Exception as e:
     db.rollback()
     print('try again')








     =======================================================================


      <!-- {% for key, value in x %}
                <div>{{key}}: {{value}}</div>
               <div class='results'><div class='isbn'><div class='author'><div class='title'><div class='year'></div></div>       
                <div>This book is {{title}} by {{author}} it was published in {{year}} and its isbn is {{isbn}}</div>  
            {% endfor %}
        {% endfor %}-->
    {% endif %}




   
    '''



bookshelf = db.execute('SELECT * FROM books')
isbn_collection = ""
for book in test[:10]:
    isbn_collection += f'{book[0]},'

print(isbn_collection)

    

review_info = requests.get(f'https://www.goodreads.com/book/review_counts.json', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'isbns': isbn_collection, 'format': 'json'})
print(reviews.json())
 

db.execute('CREATE TABLE reviews ( isbn INT PRIMARY KEY REFERENCES BOOKS(isbn), rating INT, review VARCHAR)')


def add_review(isbn):
  rating = request.forms.get('rating')
  review = request.forms.get('review body')
  review_to_add = db.execute(f'INSERT INTO reviews({isbn}, {rating}, {review})')
  stored_reviews = db.execute('SELECT * FROM reviews').fetchall()


def generate_book_page(isbn):
  # Generate page for single selected book
  try:
    counter = 0
    to_send = {}
    to_send[isbn] = {}
    book_object = db.execute(f"SELECT * FROM books WHERE isbn = '{ isbn }'").fetchall()
    review_info = requests.get(f'https://www.goodreads.com/book/review_counts.json', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'isbns': isbn, 'format': 'json'}).json()
    to_send[isbn]['isbn'] = isbn
    to_send[isbn]['title'] = book_object[0][1]
    to_send[isbn]['author'] = book_object[0][2]
    to_send[isbn]['pub_date'] = book_object[0][3]
    to_send[isbn]['ratings_count'] = review_info['books'][0]['ratings_count']
    to_send[isbn]['average_score'] = review_info['books'][0]['average_rating']
    print(to_send)
    render_template('bookpage.html', to_send)
# submitted_reviews = db.execute(f"SELECT * FROM reviews WHERE isbn = '{ isbn }'").fetchall()



#SELECT users.userid, users.username, pwd.passhash FROM users INNER JOIN pwd ON users.userid=pwd.userid