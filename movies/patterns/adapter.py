import json
from pathlib import Path

from movies.models import Movie

DEFAULT_MOVIES_JSON = Path(__file__).resolve().parent.parent / "data" / "sample_movies.json"


class JsonMovieAdapter:
    """Adapts external JSON movie records into Movie model instances."""

    @staticmethod
    def to_movie(data: dict) -> Movie:
        return Movie(
            title=data["title"],
            director=data["director"],
            release_year=int(data["release_year"]),
            genre=data["genre"],
        )

    @classmethod
    def load_from_file(cls, path=None) -> list[Movie]:
        json_path = Path(path) if path else DEFAULT_MOVIES_JSON
        with json_path.open(encoding="utf-8") as handle:
            payload = json.load(handle)

        rows = payload["movies"] if isinstance(payload, dict) else payload
        return [cls.to_movie(row) for row in rows]
