from decimal import Decimal

from movies.models import Movie


class MovieDataFactory:
    @staticmethod
    def sample_catalog():
        return [
            {"title": "The Shawshank Redemption", "director": "Frank Darabont", "release_year": 1994, "genre": "Drama", "average_rating": Decimal("9.3")},
            {"title": "The Dark Knight", "director": "Christopher Nolan", "release_year": 2008, "genre": "Action", "average_rating": Decimal("9.0")},
            {"title": "Inception", "director": "Christopher Nolan", "release_year": 2010, "genre": "Sci-Fi", "average_rating": Decimal("8.8")},
            {"title": "Parasite", "director": "Bong Joon-ho", "release_year": 2019, "genre": "Thriller", "average_rating": Decimal("8.6")},
            {"title": "Spirited Away", "director": "Hayao Miyazaki", "release_year": 2001, "genre": "Animation", "average_rating": Decimal("8.6")},
        ]

    @classmethod
    def create_all_samples(cls):
        return [Movie(**row) for row in cls.sample_catalog()]
