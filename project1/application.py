import os, requests, json

from flask import Flask, session, render_template, request, jsonify, make_response, redirect, url_for
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
app.config["SECRET_KEY"] = 'test_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['FLASK_APP'] = 'application.py'
# app.config['DATABASE_URL=postgres://ctiazebqyiyhlf:349007f1e4d3c17da2a3c149efb9ef17e521f4a38c2c0c570968c4e5735cefb1@ec2-174-129-210-249.compute-1.amazonaws.com:5432/daj1jc00ojlhg6']
app.config['JSON_SORT_KEYS'] = False
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), pool_size=10, max_overflow=20)
db = scoped_session(sessionmaker(bind=engine))

app.debug = 1

# TODO: add function to check and see if the database/table exists. If not it builds it. but if it does it loads it

def check_logged_in():
    if request.cookies.get('logged_in') == 'True':
        print('it was true')
        pass
    else:
        return  redirect(url_for('login'))



@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if session['logged_in'] == 'True':
        return render_template('homepage.html', message='Please enter search query')

    else:    
        try:
            username = ''
            password = ''
            if request.method == "POST":
                try:
                    username = request.form.get('username')
                    password = request.form.get('password')
                    try:
                        fetched_pwd = db.execute(f"SELECT pwd.passhash FROM pwd INNER JOIN users ON users.userid=pwd.userid WHERE users.username = '{username}'").fetchall()[0][0]
                        print(f'fetched password is {fetched_pwd}')
                        if password != fetched_pwd:
                            return render_template('login.html', message='no user by that name')
                    except Exception as err:
                        print('user not found')
                        return render_template('login.html', message='no user by that name')
                    
                    
                    if fetched_pwd == password:
                        res = make_response(render_template('homepage.html', message=f'Please enter search'))
                        print('test1')
                        res.set_cookie('username', f'{username}')
                        print('test2')
                        res.set_cookie('logged_in', 'True')
                        print('test3')
                        print(username, password, 'it worked')
                        session['logged_in'] = "True" 
                        session['username'] = username
                        print('test4')
                        return res

                except Exception as err:
                    print(repr(err))
                    return render_template('error.html', err = repr(err), message='error1')

            else:
                return render_template('login.html', message='please log in')
                
        except Exception as err:
            print(repr(err))
            return render_template('error.html', err = repr(err), message='error2')



@app.route("/book_page/<string:isbn>")
def generate_book_page(isbn):
    check_logged_in()
  # Generate page for single selected book
    try:
        counter = 0
        to_send = {}
        to_send[isbn] = {}
        book_object = db.execute(f"SELECT * FROM books WHERE isbn LIKE '%{isbn}%'").fetchall()
        review_info = requests.get('https://www.goodreads.com/book/review_counts.json', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'isbns': isbn, 'format': 'json'}).json()
        to_send[isbn]['isbn'] = isbn
        to_send[isbn]['title'] = book_object[0][1]
        to_send[isbn]['author'] = book_object[0][2]
        to_send[isbn]['pub_date'] = book_object[0][3]
        to_send[isbn]['ratings_count'] = review_info['books'][0]['ratings_count']
        to_send[isbn]['average_score'] = review_info['books'][0]['average_rating']
        to_send[isbn]['review_list'] = db.execute(f"SELECT * FROM reviews WHERE isbn = '{isbn}'").fetchall()
        return render_template('bookpage.html', to_send = to_send, isbn = isbn)
        
    except Exception as err:
        print(repr(err))
        return render_template('error.html', err = repr(err))
    

@app.route("/submit_review/<string:isbn>", methods=['POST'])
def add_review(isbn):
    check_logged_in()
    rating = request.form.get('user-rating')
    review = request.form.get('review-text')
    username = session['username']
    print(isbn, rating, review, username)
    session['isbn'] = isbn
    review_to_add = f"{isbn}, {rating}, {review}, {username}"
    print('review to add ', review_to_add)
    db.execute(f"INSERT INTO reviews (isbn, rating, review, username) VALUES ('{isbn}', {rating}, '{review}', '{username}')" )
    db.commit()
    #db.execute(f"INSERT INTO pwd (userid, passhash) VALUES ('{user_id}', '{password}')")
    message = 'review added'
    return redirect(f'/book_page/{isbn}')

    

@app.route("/review_data")
def review_data():
        try:
            return 'this is the data review'
        except Exception as err:
            print(repr(err))
            return render_template('error.html', err = repr(err))
    

@app.route('/api/<string:isbn>')
def api_direct(isbn):
    try:
        results = db.execute(f"SELECT * FROM books WHERE isbn LIKE '%{isbn}%'").fetchall()
        review_info = requests.get('https://www.goodreads.com/book/review_counts.json', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'isbns': isbn, 'format': 'json'}).json()
        to_send = []
        for isbn, title, author, year in results:
            temp = {'isbn': isbn, 'title': title, 'author': author, 'year': year}
            temp['ratings_count'] = review_info['books'][0]['ratings_count']
            temp['average_score'] = review_info['books'][0]['average_rating']
            to_send.append(temp)
        length = len(to_send)
        print(to_send)
        return jsonify(to_send)
    except Exception as err:
        print(err)
        return render_template('api.html', message = repr(err))


@app.route('/error')
def return_error():
    try:
        return render_template('error.html')
    except Exception as err:
        print(repr(err))
    return render_template('error.html', err = repr(err))



@app.route("/search", methods=['POST', 'GET'])
def search():
    check_logged_in()
    search_term = request.form.get('searchBar')
    if search_term == "None":
        search_term = int('0345418263')
    print(f'search term is {search_term}')
  # Generate page for single selected book
    try:
        counter = 0
        to_send = []
        isbn_list = []
        search_results = db.execute("SELECT * FROM books WHERE lower(author) LIKE '%{0}%' OR lower(title) like '%{0}%' OR isbn LIKE '%{0}%'".format(search_term)).fetchall()
        result_num = len(search_results)
        print(result_num)
         
        for x in range(result_num):
            book_object = search_results[x]
            isbn = book_object[0]
            title = book_object[1]
            author = book_object[2]
            date = book_object[3]
            review_info = requests.get('https://www.goodreads.com/book/review_counts.json', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'isbns': isbn, 'format': 'json'}).json()
            
            temp = {}
            temp['isbn'] = isbn            
            temp['title'] = title
            temp['author'] = author
            temp['pub_date'] = date
            temp['ratings_count'] = review_info['books'][0]['ratings_count']
            temp['average_score'] = review_info['books'][0]['average_rating']
            to_send.append(temp)
            isbn_list.append(isbn)
            
        print('to send = ', to_send)
        print(to_send[1])
        print('isbn list =', isbn_list)
        return render_template('search_results.html', to_send=to_send, isbn_list=isbn_list)
            
        
    except Exception as err:
        print(repr(err))
        return render_template('error.html', err = repr(err))
    



@app.route('/register', methods=["POST", "GET"])
def register():
    username = ''
    password = ''
    if request.method == "POST":
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            try:
                #check to see if user already exists
                user_check = db.execute(f"SELECT * FROM users WHERE username == '{ username }'")
                
            
            except Exception as err:
                print('no user by that name')
                db.rollback()
                #if user does not already exist then insert them into the db
                try:
                    db.execute(f"INSERT INTO users (username) VALUES ('{username}')")
                    print(f'username is {username}')
                    new_user = db.execute(f"SELECT * FROM users WHERE username = '{ username }'").fetchall()
                    print(new_user)
                    user_id = str(new_user[0][0])
                    print('userid is ' + user_id)
                    db.execute(f"INSERT INTO pwd (userid, passhash) VALUES ('{user_id}', '{password}')")
                    print('success: ' + str(db.execute(f"SELECT * FROM pwd WHERE userid = '{user_id}'").fetchall()))
                    db.commit()
                    res = make_response(render_template("homepage.html", message=f'user made {user_id}, {username}, {password}'))
                    res.set_cookie('username', username)
                    return res

                except Exception as err:
                    
                    print(repr(err))
                    db.rollback()
                    return render_template("register.html", message='Please try again')
    
        except Exception as err:
                print(repr(err))
                return render_template('error.html', err = repr(err))
    
    
    elif request.method == "GET":
        return render_template("register.html")



@app.route('/logout')
def logout():
    res = make_response(render_template("login.html", message='user logged out'))
    res.set_cookie('username', 'None', max_age=0)
    res.set_cookie('logged_in', 'False', max_age=0)
    return res

 
        
    

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


   TODO:
    @route('<path:originalPath>')
    if active_login_token == False:
        redirect(loginPage)
    else:
        redirect(originalPath)


        




   if user_token
   
   if temp_user != None:
        return render_template('index.html', message='it worked')
    return 'try again'
    
    
    
    
    
    
    
    search_target = request.form.get('searchBar')
        if search_target == "None":
            search_target = int('0345418263')
        print(f'search target is {search_target}')
        search_results = db.execute("SELECT * FROM books WHERE lower(author) LIKE '%{0}%' OR lower(title) like '%{0}%' OR isbn LIKE '%{0}%'".format(search_target)).fetchall()
        for result in list(search_results):
            print(result)
        to_send = list(search_results)
        print(to_send)
        return render_template('index.html', to_send=to_send)
    except Exception as err:
        print(repr(err))
        return render_template('error.html', err = repr(err))












    

@app.route('/search', methods=["GET", "POST"])
def search():
    search_target = request.form.get('searchBar')
    if search_target == "None":
        search_target = int('0345418263')
    print(f'search target is {search_target}')

    try:
        counter = 0
        to_send = {}
        book_object = 
        to_send[isbn] = {}
        search_results = db.execute("SELECT * FROM books WHERE lower(author) LIKE '%{0}%' OR lower(title) like '%{0}%' OR isbn LIKE '%{0}%'".format(search_target)).fetchall()
        review_info = requests.get('https://www.goodreads.com/book/review_counts.json', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'isbns': isbn_list, 'format': 'json'}).json()
        to_send[isbn]['isbn'] = isbn
        to_send[isbn]['title'] = book_object[0][1]
        to_send[isbn]['author'] = book_object[0][2]
        to_send[isbn]['pub_date'] = book_object[0][3]
        to_send[isbn]['ratings_count'] = review_info['books'][0]['ratings_count']
        to_send[isbn]['average_score'] = review_info['books'][0]['average_rating']
        print(to_send)
        return render_template('bookpage.html', to_send = to_send, isbn = isbn)
    
    except Exception as err:
        print(repr(err))
        return render_template('error.html', err = repr(err))
        
        
        
    try: 
        search_target = request.form.get('searchBar')
        if search_target == "None":
            search_target = int('0345418263')
        results = db.execute("SELECT * FROM books WHERE lower(author) LIKE '%{0}%' OR lower(title) like '%{0}%' OR isbn LIKE '%{0}%'".format(search_target)).fetchall()
        to_send = {}
        isbn_list = []
        for isbn, title, author, year in results:
            review_info = requests.get('https://www.goodreads.com/book/review_counts.json', params={'key': '7CXiGcXrotgoPlcPvEFZMw', 'isbns': isbn, 'format': 'json'}).json()
            temp = {}
            temp = {'isbn': isbn, 'title': title, 'author': author, 'year': year}
            temp['ratings_count'] = review_info['books'][0]['ratings_count']
            temp['average_score'] = review_info['books'][0]['average_rating']
            to_send[isbn] = temp
            isbn_list.append(isbn)
        
        print(to_send)
        return render_template('index.html', to_send= json.dumps(to_send), isbn_list=isbn_list)

    except Exception as err:
        print(repr(err))
        return render_template('error.html', err = repr(err))


'''



def create_post(book_object, review_info):

    post = {}
    post['isbn'] = book_object[0]
    post['title'] = book_object[1]
    post['author'] = book_object[2]
    post['year'] = book_object[3]
    post['review_count'] = review_info['books']['ratings_count']
    post['average_score'] = review_info['books']['average_rating']


#goodreads api sample
#{'books': [{'id': 846984, 'isbn': '0375913750', 'isbn13': '9780375913754', 'ratings_count': 35755, 'reviews_count': 60079, 'text_reviews_count': 2853, 'work_ratings_count': 38058, 'work_reviews_count': 64427, 'work_text_reviews_count': 3174, 'average_rating': '3.82'}]}

#db response example
#[('0553803700', 'I, Robot', 'Isaac Asimov', 1950)]




# test = db.execute(f"SELECT pwd.passhash FROM pwd INNER JOIN users ON users.userid=pwd.userid WHERE users.username = '{username}'").fetchall()[0][0]

# if 'username' in session