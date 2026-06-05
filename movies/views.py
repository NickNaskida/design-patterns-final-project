from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
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

def edit_movie(request, pk):
    service = MovieService()
    movie = service.get_movie(pk)
    if not movie:
        raise Http404("Movie not found")
        
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            service.update_movie(pk, **form.cleaned_data)
            return redirect("movie_list")
    else:
        form = MovieForm(instance=movie)
        
    return render(request, "movies/edit_movie.html", {"form": form, "movie": movie})

def delete_movie(request, pk):
    service = MovieService()
    if request.method == "POST":
        if service.delete_movie(pk):
            return redirect("movie_list")
        raise Http404("Movie not found")
        
    movie = service.get_movie(pk)
    if not movie:
        raise Http404("Movie not found")
        
    return render(request, "movies/delete_confirm.html", {"movie": movie})