from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
