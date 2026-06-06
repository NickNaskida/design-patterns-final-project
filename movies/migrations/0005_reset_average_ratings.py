from decimal import Decimal

from django.db import migrations
from django.db.models import Avg


def reset_average_ratings(apps, schema_editor):
    Movie = apps.get_model("movies", "Movie")
    Rating = apps.get_model("movies", "Rating")

    Movie.objects.update(average_rating=Decimal("0"))

    for movie in Movie.objects.all():
        average = (
            Rating.objects.filter(movie_id=movie.pk).aggregate(avg=Avg("score"))["avg"]
        )
        if average is not None:
            movie.average_rating = round(average, 1)
            movie.save(update_fields=["average_rating"])


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_rating"),
    ]

    operations = [
        migrations.RunPython(reset_average_ratings, migrations.RunPython.noop),
    ]
