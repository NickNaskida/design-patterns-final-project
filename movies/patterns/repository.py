from abc import ABC, abstractmethod

from django.db.models import Avg, Q

from movies.models import Movie, Rating


ALLOWED_SORT_FIELDS = {
    "title": "title",
    "-title": "-title",
    "director": "director",
    "-director": "-director",
    "release_year": "release_year",
    "-release_year": "-release_year",
    "average_rating": "average_rating",
    "-average_rating": "-average_rating",
}


def _ordered(queryset, sort=None):
    order = ALLOWED_SORT_FIELDS.get(sort, "title")
    return queryset.order_by(order)


class MovieRepository(ABC):
    @abstractmethod
    def get_all(self, sort=None):
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
    def search(self, query, sort=None):
        pass

    @abstractmethod
    def count(self):
        pass


class DjangoMovieRepository(MovieRepository):
    def get_all(self, sort=None):
        return _ordered(Movie.objects.all(), sort)

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

    def search(self, query, sort=None):
        queryset = Movie.objects.filter(
            Q(title__icontains=query) | Q(director__icontains=query)
        )
        return _ordered(queryset, sort)

    def count(self):
        return Movie.objects.count()


class RatingRepository(ABC):
    @abstractmethod
    def get_user_rating(self, user, movie_id):
        pass

    @abstractmethod
    def get_user_ratings_for_movies(self, user, movie_ids):
        pass

    @abstractmethod
    def get_ratings_for_movies(self, movie_ids):
        pass

    @abstractmethod
    def upsert(self, user, movie, score):
        pass

    @abstractmethod
    def recalculate_average(self, movie):
        pass


class DjangoRatingRepository(RatingRepository):
    def get_user_rating(self, user, movie_id):
        try:
            return Rating.objects.get(user=user, movie_id=movie_id)
        except Rating.DoesNotExist:
            return None

    def get_user_ratings_for_movies(self, user, movie_ids):
        if not movie_ids:
            return {}
        ratings = Rating.objects.filter(user=user, movie_id__in=movie_ids)
        return {rating.movie_id: rating for rating in ratings}

    def get_ratings_for_movies(self, movie_ids):
        if not movie_ids:
            return {}
        ratings = (
            Rating.objects.filter(movie_id__in=movie_ids)
            .select_related("user")
            .order_by("user__username")
        )
        grouped = {}
        for rating in ratings:
            grouped.setdefault(rating.movie_id, []).append(rating)
        return grouped

    def upsert(self, user, movie, score):
        rating, _ = Rating.objects.update_or_create(
            user=user,
            movie=movie,
            defaults={"score": score},
        )
        rating.full_clean()
        rating.save()
        return rating

    def recalculate_average(self, movie):
        result = Rating.objects.filter(movie=movie).aggregate(avg=Avg("score"))
        average = result["avg"]
        movie.average_rating = round(average, 1) if average is not None else 0
        movie.save(update_fields=["average_rating"])
        return movie
