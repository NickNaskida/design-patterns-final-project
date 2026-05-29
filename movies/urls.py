from django.urls import path
from movies import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("add/", views.add_movie, name="add_movie"),
]