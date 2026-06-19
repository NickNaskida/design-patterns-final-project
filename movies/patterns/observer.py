from movies.patterns.repository import DjangoRatingRepository


class AverageRatingObserver:
    """Observer: recalculates Movie.average_rating when notified of a rating change."""

    def __init__(self, rating_repo=None):
        self.rating_repo = rating_repo or DjangoRatingRepository()

    def on_rating_changed(self, movie):
        self.rating_repo.recalculate_average(movie)
