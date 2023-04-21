from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    game_info = {"gameId": game_id, "board": game.board}


    return jsonify(game_info)

@app.post("/api/score-word")
def get_score():
    """accept a POST request with JSON for the game id and the word.
       It should check if the word is legal"""

    # get the form data word input 
    word = request.json["word"]
    game_id = request.json["gameId"]
    game = games[game_id] 
    print('word ===>', word)

    if not game.is_word_in_word_list(word):
        result = {"result": "not-word"}
    elif not game.check_word_on_board(word):
        result = {"result": "not-on-board"}
    else:
        result = {"result": "ok"}

    return jsonify(result)



