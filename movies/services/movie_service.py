from movies.patterns.factory import MovieDataFactory
from movies.patterns.repository import DjangoMovieRepository


class MovieService:
    def __init__(self, repo=None):
        self.repo = repo or DjangoMovieRepository()

    def list_movies(self):
        return self.repo.get_all()

    def seed_sample_data(self):
        if self.repo.count() > 0:
            return 0
        n = 0
        for movie in MovieDataFactory.create_all_samples():
            self.repo.save(movie)
            n += 1
        return n
