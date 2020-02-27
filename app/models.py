from flask import url_for
from sqlalchemy.schema import Table

from app import db


class PaginatedAPIMixin:
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total,
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


db.reflect()


class Platform(db.Model):
    __tablename__ = 'gamecatalog_platform'


class Genre(db.Model):
    __tablename__ = 'gamecatalog_genre'


class Keyword(db.Model):
    __tablename__ = 'gamecatalog_keyword'


class Screenshot(db.Model):
    __tablename__ = 'gamecatalog_screenshot'


class Game(PaginatedAPIMixin, db.Model):
    __tablename__ = 'gamecatalog_game'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cover_url': self.cover_url,
            'summary': self.summary,
            'release_data': self.release_date,
            'rating': self.rating,
            'rating_count': self.rating_count,
            'aggregated_rating': self.aggregated_rating,
            'aggregated_rating_count': self.aggregated_rating_count,
            'screenshots': [screenshot.image_url for screenshot in self.screenshots],
            'platforms': [platform.name for platform in self.platforms],
            'genres': [genre.slug for genre in self.genres],
            'keywords': [keyword.slug for keyword in self.keywords],
        }


class User(db.Model):
    __tablename__ = 'gamecatalog_user'


class Favourite(PaginatedAPIMixin, db.Model):
    __tablename__ = 'gamecatalog_favourite'

    def to_dict(self):
        return {
            'game': self.game.to_dict(),
            'is_deleted': self.is_deleted,
        }


game_platforms_association = db.Model.metadata.tables['gamecatalog_game_platforms']
game_genres_association = db.Model.metadata.tables['gamecatalog_game_genres']
game_keywords_association = db.Model.metadata.tables['gamecatalog_game_keywords']

Game.platforms = db.relationship('Platform', secondary=game_platforms_association, backref='games')
Game.genres = db.relationship('Genre', secondary=game_genres_association, backref='games')
Game.keywords = db.relationship('Keyword', secondary=game_keywords_association, backref='games')

Game.screenshots = db.relationship('Screenshot', backref='game', lazy='dynamic')

Favourite.game = db.relationship('Game', backref='favourites')
Favourite.user = db.relationship('User', backref='favourites')
