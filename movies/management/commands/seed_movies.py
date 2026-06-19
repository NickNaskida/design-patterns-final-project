from django.core.management.base import BaseCommand

from movies.services.movie_service import MovieService


class Command(BaseCommand):
    help = "Load sample movies from JSON (skips if the database already has movies)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            dest="json_path",
            help="Path to a JSON file with a top-level movies array.",
        )

    def handle(self, *args, **options):
        n = MovieService().import_from_json(options.get("json_path"))
        if n:
            self.stdout.write(f"added {n} movies")
        else:
            self.stdout.write("nothing to add (db not empty?)")
