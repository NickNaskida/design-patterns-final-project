from abc import ABC, abstractmethod

from movies.models import Movie


class MovieRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, movie):
        pass

    @abstractmethod
    def count(self):
        pass


class DjangoMovieRepository(MovieRepository):
    def get_all(self):
        return Movie.objects.all()

    def save(self, movie):
        movie.save()
        return movie

    def count(self):
        return Movie.objects.count()
