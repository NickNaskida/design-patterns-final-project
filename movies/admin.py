from django.contrib import admin

from movies.models import Movie, Rating

admin.site.register(Movie)
admin.site.register(Rating)
