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
    def search(self, query):
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
        movie.full_clean()
        movie.save()
        return movie

    def delete(self, movie):
        movie.delete()

    def search(self, query):
        from django.db.models import Q
        return Movie.objects.filter(
            Q(title__icontains=query) | Q(director__icontains=query)
        )

    def count(self):
        return Movie.objects.count()
