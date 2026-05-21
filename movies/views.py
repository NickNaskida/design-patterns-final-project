from django.shortcuts import render

from movies.services.movie_service import MovieService


def movie_list(request):
    movies = MovieService().list_movies()
    return render(request, "movies/movie_list.html", {"movies": movies})
