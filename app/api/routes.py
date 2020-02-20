from flask import jsonify, request

from app import db
from app.api import bp
from app.models import Game, Favourite, User


@bp.route('/')
def index():
    return 'Hello World'


@bp.route('/games')
def get_games():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Game.to_collection_dict(Game.query, page, per_page, 'api.get_games')
    return jsonify(data)


@bp.route('/games/<int:id>')
def get_game(id):
    return jsonify(Game.query.get_or_404(id).to_dict())


@bp.route('/favs/<int:user_id>')
def get_fav_games(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Favourite.to_collection_dict(Favourite.query.filter_by(user=user), \
        page, per_page, 'api.get_fav_games', user_id=user_id)
    return jsonify(data)
