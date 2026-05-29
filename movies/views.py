from django.shortcuts import render, redirect
from movies.services.movie_service import MovieService
from movies.forms import MovieForm

def movie_list(request):
    movies = MovieService().list_movies()
    return render(request, "movies/movie_list.html", {"movies": movies})

def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            MovieService().add_movie(**form.cleaned_data)
            return redirect("movie_list")
    else:
        form = MovieForm()
        
    return render(request, "movies/add_movie.html", {"form": form})