import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "8e8195a6d7e67321b7659fe6"
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index3.html")

@socketio.on('submit vote')
def vote(data):
    selection = data["selection"]
    emit("announce vote", {"selection" : selection}, broadcast=True)
