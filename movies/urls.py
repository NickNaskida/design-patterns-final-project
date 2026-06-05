from django.urls import path
from movies import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("add/", views.add_movie, name="add_movie"),
    path("edit/<int:pk>/", views.edit_movie, name="edit_movie"),
    path("delete/<int:pk>/", views.delete_movie, name="delete_movie"),
]