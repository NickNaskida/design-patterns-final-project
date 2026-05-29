from movies.patterns.factory import MovieDataFactory
from movies.patterns.repository import DjangoMovieRepository
from movies.models import Movie

class MovieService:
    def __init__(self, repo=None):
        self.repo = repo or DjangoMovieRepository()

    def list_movies(self):
        return self.repo.get_all()

    def add_movie(self, **kwargs):
        movie = Movie(**kwargs)
        return self.repo.save(movie)

    def seed_sample_data(self):
        if self.repo.count() > 0:
            return 0
        n = 0
        for movie in MovieDataFactory.create_all_samples():
            self.repo.save(movie)
            n += 1
        return n