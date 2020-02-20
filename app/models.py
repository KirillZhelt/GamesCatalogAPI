from sqlalchemy.schema import Table

from app import db

db.reflect()


class Platform(db.Model):
    __tablename__ = 'gamecatalog_platform'


class Genre(db.Model):
    __tablename__ = 'gamecatalog_genre'


class Keyword(db.Model):
    __tablename__ = 'gamecatalog_keyword'


class Screenshot(db.Model):
    __tablename__ = 'gamecatalog_screenshot'


class Game(db.Model):
    __tablename__ = 'gamecatalog_game'


class Favourite(db.Model):
    __tablename__ = 'gamecatalog_favourite'


game_platforms_association = db.Model.metadata.tables['gamecatalog_game_platforms']
game_genres_association = db.Model.metadata.tables['gamecatalog_game_genres']
game_keywords_association = db.Model.metadata.tables['gamecatalog_game_keywords']

Game.platforms = db.relationship('Platform', secondary=game_platforms_association, backref='games')
Game.genres = db.relationship('Genre', secondary=game_genres_association, backref='games')
Game.keywords = db.relationship('Keyword', secondary=game_keywords_association, backref='games')

Game.screenshots = db.relationship('Screenshot', backref='game', lazy='dynamic')

Favourite.game = db.relationship('Game', backref='favourites')
