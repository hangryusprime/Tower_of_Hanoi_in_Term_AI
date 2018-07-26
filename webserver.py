#!/usr/bin/env python3
import sys
from flask import app, jsonify, Flask
from hanoi import *
from settings import who, ai, log, web, delay, amount
app = Flask(__name__)
game = Game(who=who, ai=ai, log=log, delay=delay, web=web, amount=amount)



@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_game_state')
def get_state():
    f = { "board1": game.pyramids }
    return jsonify(**f)
   
def run(game_):
    global game
    if game_:
        game = game_
        #print("Starting server")
        app.run()
            
    else: raise Exception('Game is Undefined')

if __name__ == '__main__':
    app.run()
    


