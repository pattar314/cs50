import os

from flask import Flask

from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

def __init__(self):
    self.messages = {}
    self.users = {}
    self.channels = {}
    

@app.route("/")
def index():
    return "Project 2: TODO"


@app.route("/createChannel")
def createChannel():
    pass


@app.route("/registerUser")
def registerUser():
    pass


@app.route("/login")
def login():
    pass


@app.route("/logout")
def logout():
    pass


def send_message():
    pass

@app.route("/")
