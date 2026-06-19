from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode

from movies.forms import MovieForm, RatingForm
from movies.patterns.repository import ALLOWED_SORT_FIELDS
from movies.patterns.strategy import SEARCH_STRATEGIES
from movies.services.movie_service import MovieService
from movies.services.rating_service import RatingService


def staff_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped


def movie_list(request):
    query = request.GET.get("q")
    sort = request.GET.get("sort", "title")
    search_strategy = request.GET.get("search_by", "combined")
    if sort not in ALLOWED_SORT_FIELDS:
        sort = "title"
    if search_strategy not in SEARCH_STRATEGIES:
        search_strategy = "combined"

    service = MovieService()
    if query:
        movies = service.search_movies(query, sort=sort, search_strategy=search_strategy)
    else:
        movies = service.list_movies(sort=sort)

    user_ratings = {}
    if request.user.is_authenticated:
        movie_ids = [movie.pk for movie in movies]
        user_ratings = RatingService().get_user_ratings(request.user, movie_ids)

    list_params = {}
    if query:
        list_params["q"] = query
    if sort != "title":
        list_params["sort"] = sort
    if search_strategy != "combined":
        list_params["search_by"] = search_strategy

    for movie in movies:
        rating = user_ratings.get(movie.pk)
        movie.user_score = rating.score if rating else None
        ratings_url = reverse("movie_ratings", args=[movie.pk])
        if list_params:
            ratings_url = f"{ratings_url}?{urlencode(list_params)}"
        movie.ratings_url = ratings_url

    return render(
        request,
        "movies/movie_list.html",
        {
            "movies": movies,
            "query": query,
            "sort": sort,
            "search_strategy": search_strategy,
        },
    )


@staff_required
def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            MovieService().add_movie(**form.cleaned_data)
            return redirect("movie_list")
    else:
        form = MovieForm()

    return render(request, "movies/add_movie.html", {"form": form})


@staff_required
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


@staff_required
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


def movie_ratings(request, pk):
    service = MovieService()
    movie = service.get_movie(pk)
    if not movie:
        raise Http404("Movie not found")

    ratings = RatingService().get_movie_ratings([pk]).get(pk, [])
    query = request.GET.get("q")
    sort = request.GET.get("sort", "title")
    search_strategy = request.GET.get("search_by", "combined")
    if sort not in ALLOWED_SORT_FIELDS:
        sort = "title"
    if search_strategy not in SEARCH_STRATEGIES:
        search_strategy = "combined"

    list_params = {}
    if query:
        list_params["q"] = query
    if sort != "title":
        list_params["sort"] = sort
    if search_strategy != "combined":
        list_params["search_by"] = search_strategy
    list_url = reverse("movie_list")
    if list_params:
        list_url = f"{list_url}?{urlencode(list_params)}"

    return render(
        request,
        "movies/movie_ratings.html",
        {
            "movie": movie,
            "ratings": ratings,
            "list_url": list_url,
        },
    )


@login_required
def rate_movie(request, pk):
    movie = MovieService().get_movie(pk)
    if not movie:
        raise Http404("Movie not found")

    redirect_params = {}
    query = request.POST.get("q") or request.GET.get("q")
    sort = request.POST.get("sort") or request.GET.get("sort", "title")
    search_strategy = request.POST.get("search_by") or request.GET.get("search_by", "combined")
    if query:
        redirect_params["q"] = query
    if sort and sort in ALLOWED_SORT_FIELDS and sort != "title":
        redirect_params["sort"] = sort
    if search_strategy in SEARCH_STRATEGIES and search_strategy != "combined":
        redirect_params["search_by"] = search_strategy

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            RatingService().rate_movie(
                request.user,
                movie.pk,
                form.cleaned_data["score"],
            )

    list_url = reverse("movie_list")
    if redirect_params:
        list_url = f"{list_url}?{urlencode(redirect_params)}"
    return redirect(list_url)
