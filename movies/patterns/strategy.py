from abc import ABC, abstractmethod

from django.db.models import Q


class SearchStrategy(ABC):
    @abstractmethod
    def build_filter(self, query: str) -> Q:
        pass


class CombinedSearchStrategy(SearchStrategy):
    def build_filter(self, query: str) -> Q:
        return Q(title__icontains=query) | Q(director__icontains=query)


class TitleSearchStrategy(SearchStrategy):
    def build_filter(self, query: str) -> Q:
        return Q(title__icontains=query)


class DirectorSearchStrategy(SearchStrategy):
    def build_filter(self, query: str) -> Q:
        return Q(director__icontains=query)


class GenreSearchStrategy(SearchStrategy):
    def build_filter(self, query: str) -> Q:
        return Q(genre__icontains=query)


SEARCH_STRATEGIES = {
    "combined": CombinedSearchStrategy(),
    "title": TitleSearchStrategy(),
    "director": DirectorSearchStrategy(),
    "genre": GenreSearchStrategy(),
}

DEFAULT_SEARCH_STRATEGY = "combined"
