from decimal import Decimal

from django.core.exceptions import ValidationError

from movies.patterns.observer import AverageRatingObserver
from movies.patterns.repository import DjangoMovieRepository, DjangoRatingRepository


class RatingService:
    def __init__(self, movie_repo=None, rating_repo=None, observers=None):
        self.movie_repo = movie_repo or DjangoMovieRepository()
        self.rating_repo = rating_repo or DjangoRatingRepository()
        self.observers = observers if observers is not None else [AverageRatingObserver()]

    def rate_movie(self, user, movie_id, score):
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            return None

        rating = self.rating_repo.upsert(user, movie, score)
        for observer in self.observers:
            observer.on_rating_changed(movie)
        return rating

    def get_user_ratings(self, user, movie_ids):
        if not user.is_authenticated:
            return {}
        return self.rating_repo.get_user_ratings_for_movies(user, movie_ids)

    def get_movie_ratings(self, movie_ids):
        return self.rating_repo.get_ratings_for_movies(movie_ids)

    def validate_score(self, score):
        value = Decimal(str(score))
        if value < 0 or value > 10:
            raise ValidationError("Rating must be between 0 and 10.")
        return value
