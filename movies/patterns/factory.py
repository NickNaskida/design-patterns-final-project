from movies.patterns.adapter import JsonMovieAdapter


class MovieDataFactory:
    @classmethod
    def create_all_samples(cls):
        return JsonMovieAdapter.load_from_file()
