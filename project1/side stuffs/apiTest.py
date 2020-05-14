import requests, json, os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



def build_book_page(search_target):
    #search for book and display results to choose from
    results = db.execute(f"SELECT * FROM books WHERE lower(author) LIKE '%{ search_target }%' OR lower(title) like '%{ search_target }%' OR isbn LIKE '%{ search_target }%'")
    print(list(results))


search_target = input('\n\nPlease enter search:    \n\n')
print('------------------')
print('\n')

#build_book_page(search_target)
book_page = {}
res = requests.get(f'https://www.goodreads.com/book/review_counts.json', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'isbns': search_target, 'format': 'json', 'user_id': 52610480})
search_results = res.json()['books']
print(search_results)


'''
#res = requests.get(f'https://www.goodreads.com/book/isbn/', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'format': 'json', 'user_id': 52610480, 'isbn': search})

if (res.status_code == 200):
    target = res.json()
    print(target)
    print('-------------------------------\n\n')
else:
    print(res)
    
    
    
    
    
  #  '0553803700'

'''

