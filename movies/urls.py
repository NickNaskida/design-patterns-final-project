from django.urls import path
from movies import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("add/", views.add_movie, name="add_movie"),
    path("<int:pk>/ratings/", views.movie_ratings, name="movie_ratings"),
    path("edit/<int:pk>/", views.edit_movie, name="edit_movie"),
    path("delete/<int:pk>/", views.delete_movie, name="delete_movie"),
    path("rate/<int:pk>/", views.rate_movie, name="rate_movie"),
]