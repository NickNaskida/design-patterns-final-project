from django.core.management.base import BaseCommand

from movies.services.movie_service import MovieService


class Command(BaseCommand):
    help = "load sample movies"

    def handle(self, *args, **options):
        n = MovieService().seed_sample_data()
        if n:
            self.stdout.write(f"added {n} movies")
        else:
            self.stdout.write("nothing to add (db not empty?)")
