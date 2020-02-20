from flask import jsonify

from app import db
from app.api import bp
from app.models import Game, Favourite


@bp.route('/')
def index():
    print(Game.query.first().favourites)
    return 'Hello World'


@bp.route('/games')
def get_games():
    games = [{'id': 5, 'name': 'FIFA 20'}]
    return jsonify(games)


@bp.route('/games/<int:id>')
def get_game(id):
    game = {'id': id, 'name': 'FIFA 20'}
    return jsonify(game)


@bp.route('/favs/<int:user_id>')
def get_fav_games(user_id):
    games = [{'id': 5, 'name': 'FIFA 20'}, {'id': 25, 'name': 'GTA V'}]
    return jsonify(games)
