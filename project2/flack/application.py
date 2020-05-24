import os

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {
    main_channel = {
        # message format is username : message_body
  "messages" : [
      { "tester1" : "this is not a test"},
      { "tester2" : "actually this is a test"},
    ]  },
}



@app.route("/")
def index():
    return "Project 2: TODO"


def create_user():
    pass


def delete_user():
    pass


def login():
    pass


def logout():
    pass


def create_channel():
    pass


def delete_channel():
    pass


def list_channels():
    pass


def change_channel():
    pass


def make_message():
    pass


def delete_message():
    pass


def retrieve_messages():
    pass

