import os, requests, json

from flask import Flask, session, render_template, request, jsonify, make_response, redirect
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
# app.config['DATABASE_URL=postgres://ctiazebqyiyhlf:349007f1e4d3c17da2a3c149efb9ef17e521f4a38c2c0c570968c4e5735cefb1@ec2-174-129-210-249.compute-1.amazonaws.com:5432/daj1jc00ojlhg6']
app.config['JSON_SORT_KEYS'] = False
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), pool_size=10, max_overflow=20)
db = scoped_session(sessionmaker(bind=engine))

app.debug = 1

@app.route('/', methods=["GET", "POST"])
def login():
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
                
                except Exception as err:
                    print('user not found')
                    return render_template('log.html', message='no user by that name')
                
                
                if fetched_pwd == password:
                    res = make_response(render_template('log.html', message=f''))
                    print('test1')
                    res.set_cookie('username', f'{username}')
                    print('test2')
                    res.set_cookie('logged_in', 'True')
                    print('test3')
                    print(username, password, 'it worked') 
                    print('test4')
                    return res

            except Exception as err:
                print(repr(err))
                return render_template('error.html', err = repr(err), message='error1')

        else:
            return render_template('log.html', message="please enter test user")
    except Exception as err:
        print(repr(err))
        return render_template('error.html', err = repr(err), message='error2')





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
    res = make_response(render_template("log.html", message='user logged out'))
    res.set_cookie('username', 'None', max_age=0)
    res.set_cookie('logged_in', 'False', max_age=0)
    return res

