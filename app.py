from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/host/<id>")
def hostLobby(id):
    return render_template("hostLobby.html")


@app.route('/player/<name>/<pin>')
def playerLobby(name, pin):
    return render_template("playerLobby.html")


# @app.route("/host/game", defaults={"id": None})
@app.route("/host/game/<id>")
def host(id):
    return render_template("hostGame.html")


# @app.route("/player/game/", defaults={"id": None})
@app.route("/player/game/<id>")
def player(id):
    return render_template("playerGame.html")
