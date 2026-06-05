from abc import ABC, abstractmethod

from movies.models import Movie


class MovieRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def save(self, movie):
        pass

    @abstractmethod
    def delete(self, movie):
        pass

    @abstractmethod
    def count(self):
        pass


class DjangoMovieRepository(MovieRepository):
    def get_all(self):
        return Movie.objects.all()

    def get_by_id(self, id):
        try:
            return Movie.objects.get(pk=id)
        except Movie.DoesNotExist:
            return None

    def save(self, movie):
        movie.save()
        return movie

    def delete(self, movie):
        movie.delete()

    def count(self):
        return Movie.objects.count()
