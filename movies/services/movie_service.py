from movies.patterns.adapter import JsonMovieAdapter
from movies.patterns.repository import DjangoMovieRepository
from movies.models import Movie


class MovieService:
    def __init__(self, repo=None):
        self.repo = repo or DjangoMovieRepository()

    def list_movies(self, sort=None):
        return self.repo.get_all(sort=sort)

    def search_movies(self, query, sort=None, search_strategy=None):
        if not query:
            return self.list_movies(sort=sort)
        return self.repo.search(query, sort=sort, search_strategy=search_strategy)

    def get_movie(self, movie_id):
        return self.repo.get_by_id(movie_id)

    def add_movie(self, **kwargs):
        kwargs.pop("average_rating", None)
        movie = Movie(**kwargs)
        return self.repo.save(movie)

    def update_movie(self, movie_id, **kwargs):
        kwargs.pop("average_rating", None)
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

    def import_from_json(self, path=None):
        if self.repo.count() > 0:
            return 0
        n = 0
        for movie in JsonMovieAdapter.load_from_file(path):
            self.repo.save(movie)
            n += 1
        return n

    def seed_sample_data(self):
        return self.import_from_json()