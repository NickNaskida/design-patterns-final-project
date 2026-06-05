from movies.patterns.factory import MovieDataFactory
from movies.patterns.repository import DjangoMovieRepository
from movies.models import Movie

class MovieService:
    def __init__(self, repo=None):
        self.repo = repo or DjangoMovieRepository()

    def list_movies(self):
        return self.repo.get_all()

    def search_movies(self, query):
        if not query:
            return self.list_movies()
        return self.repo.search(query)

    def get_movie(self, movie_id):
        return self.repo.get_by_id(movie_id)

    def add_movie(self, **kwargs):
        movie = Movie(**kwargs)
        return self.repo.save(movie)

    def update_movie(self, movie_id, **kwargs):
        movie = self.repo.get_by_id(movie_id)
        if movie:
            for key, value in kwargs.items():
                setattr(movie, key, value)
            return self.repo.save(movie)
        return None

    def delete_movie(self, movie_id):
        movie = self.repo.get_by_id(movie_id)
        if movie:
            self.repo.delete(movie)
            return True
        return False

    def seed_sample_data(self):
        if self.repo.count() > 0:
            return 0
        n = 0
        for movie in MovieDataFactory.create_all_samples():
            self.repo.save(movie)
            n += 1
        return n