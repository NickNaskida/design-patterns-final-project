from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from movies.forms import MovieForm, RatingForm
from movies.models import Movie, Rating
from movies.patterns.adapter import JsonMovieAdapter
from movies.patterns.observer import AverageRatingObserver
from movies.services.movie_service import MovieService
from movies.services.rating_service import RatingService


class MovieTests(TestCase):
    def setUp(self):
        self.service = MovieService()
        self.movie = self.service.add_movie(
            title="Inception",
            director="Christopher Nolan",
            release_year=2010,
            genre="Sci-Fi",
        )
        self.client = Client()

    def test_list_movies(self):
        movies = self.service.list_movies()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0].title, "Inception")

    def test_get_movie(self):
        movie = self.service.get_movie(self.movie.pk)
        self.assertEqual(movie.title, "Inception")

    def test_update_movie_service(self):
        self.service.update_movie(self.movie.pk, title="Inception Updated")
        updated_movie = self.service.get_movie(self.movie.pk)
        self.assertEqual(updated_movie.title, "Inception Updated")

    def test_delete_movie_service(self):
        success = self.service.delete_movie(self.movie.pk)
        self.assertTrue(success)
        self.assertIsNone(self.service.get_movie(self.movie.pk))

    def test_edit_movie_view(self):
        admin = User.objects.create_user(username="admin", password="pass", is_staff=True)
        self.client.login(username="admin", password="pass")

        response = self.client.get(reverse("edit_movie", args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("edit_movie", args=[self.movie.pk]),
            {
                "title": "Inception Edited",
                "director": "Christopher Nolan",
                "release_year": 2010,
                "genre": "Sci-Fi",
            },
        )
        self.assertRedirects(response, reverse("movie_list"))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Inception Edited")

    def test_edit_movie_view_requires_staff(self):
        user = User.objects.create_user(username="regular", password="pass")
        self.client.login(username="regular", password="pass")
        response = self.client.get(reverse("edit_movie", args=[self.movie.pk]))
        self.assertEqual(response.status_code, 403)

    def test_edit_movie_view_requires_login(self):
        response = self.client.get(reverse("edit_movie", args=[self.movie.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_add_movie_view(self):
        admin = User.objects.create_user(username="admin", password="pass", is_staff=True)
        self.client.login(username="admin", password="pass")

        response = self.client.get(reverse("add_movie"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("add_movie"),
            {
                "title": "New Film",
                "director": "New Director",
                "release_year": 2024,
                "genre": "Drama",
            },
        )
        self.assertRedirects(response, reverse("movie_list"))
        self.assertTrue(Movie.objects.filter(title="New Film").exists())

    def test_add_movie_view_requires_staff(self):
        user = User.objects.create_user(username="regular", password="pass")
        self.client.login(username="regular", password="pass")
        response = self.client.get(reverse("add_movie"))
        self.assertEqual(response.status_code, 403)

    def test_add_movie_view_requires_login(self):
        response = self.client.get(reverse("add_movie"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_movie_view(self):
        admin = User.objects.create_user(username="admin", password="pass", is_staff=True)
        self.client.login(username="admin", password="pass")

        response = self.client.get(reverse("delete_movie", args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("delete_movie", args=[self.movie.pk]))
        self.assertRedirects(response, reverse("movie_list"))
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())

    def test_delete_movie_view_requires_staff(self):
        user = User.objects.create_user(username="regular", password="pass")
        self.client.login(username="regular", password="pass")
        response = self.client.post(reverse("delete_movie", args=[self.movie.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Movie.objects.filter(pk=self.movie.pk).exists())

    def test_search_movies_service(self):
        self.service.add_movie(
            title="The Dark Knight",
            director="Christopher Nolan",
            release_year=2008,
            genre="Action",
        )
        results = self.service.search_movies("Inception")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Inception")

        results = self.service.search_movies("Nolan")
        self.assertEqual(len(results), 2)

    def test_search_movies_view(self):
        self.service.add_movie(
            title="The Dark Knight",
            director="Christopher Nolan",
            release_year=2008,
            genre="Action",
        )
        response = self.client.get(reverse("movie_list"), {"q": "Dark"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Dark Knight")
        self.assertNotContains(response, "Inception")

    def test_sort_movies_by_rating(self):
        user = User.objects.create_user(username="sorter", password="pass")
        rating_service = RatingService()
        low = self.service.add_movie(
            title="Low Rated",
            director="Director A",
            release_year=2000,
            genre="Drama",
        )
        high = self.service.add_movie(
            title="High Rated",
            director="Director B",
            release_year=2001,
            genre="Drama",
        )
        rating_service.rate_movie(user, high.pk, Decimal("9.0"))
        rating_service.rate_movie(user, low.pk, Decimal("2.0"))
        rating_service.rate_movie(user, self.movie.pk, Decimal("4.0"))

        movies = list(self.service.list_movies(sort="-average_rating"))
        self.assertEqual(movies[0].pk, high.pk)
        self.assertEqual(movies[-1].pk, low.pk)

    def test_sort_movies_view(self):
        self.service.add_movie(
            title="Zulu",
            director="Director",
            release_year=2000,
            genre="Drama",
        )
        response = self.client.get(reverse("movie_list"), {"sort": "-title"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="-title" selected')

    def test_movie_form_excludes_average_rating(self):
        form = MovieForm(
            data={
                "title": "Test Movie",
                "director": "Test Director",
                "release_year": 2022,
                "genre": "Drama",
            }
        )
        self.assertTrue(form.is_valid())

    def test_service_ignores_average_rating_on_create(self):
        movie = self.service.add_movie(
            title="Test Movie",
            director="Test Director",
            release_year=2022,
            genre="Drama",
            average_rating=Decimal("9.5"),
        )
        self.assertEqual(movie.average_rating, Decimal("0"))

    def test_seed_sample_data_starts_at_zero(self):
        Movie.objects.all().delete()
        added = self.service.seed_sample_data()
        self.assertEqual(added, 5)
        self.assertTrue(
            all(movie.average_rating == Decimal("0") for movie in self.service.list_movies())
        )


class RatingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.other_user = User.objects.create_user(username="bob", password="pass1234")
        self.movie = MovieService().add_movie(
            title="Inception",
            director="Christopher Nolan",
            release_year=2010,
            genre="Sci-Fi",
        )
        self.rating_service = RatingService()
        self.client = Client()

    def test_rate_movie_updates_average(self):
        self.rating_service.rate_movie(self.user, self.movie.pk, Decimal("8.0"))
        self.rating_service.rate_movie(self.other_user, self.movie.pk, Decimal("6.0"))

        self.movie.refresh_from_db()
        self.assertEqual(self.movie.average_rating, Decimal("7.0"))
        self.assertEqual(Rating.objects.count(), 2)

    def test_rate_movie_overwrites_existing_user_rating(self):
        self.rating_service.rate_movie(self.user, self.movie.pk, Decimal("5.0"))
        self.rating_service.rate_movie(self.user, self.movie.pk, Decimal("9.0"))

        self.movie.refresh_from_db()
        self.assertEqual(self.movie.average_rating, Decimal("9.0"))
        self.assertEqual(Rating.objects.count(), 1)

    def test_rating_form_validation(self):
        form = RatingForm(data={"score": 11.0})
        self.assertFalse(form.is_valid())

        form = RatingForm(data={"score": 7.5})
        self.assertTrue(form.is_valid())

    def test_rate_movie_view_requires_login(self):
        response = self.client.post(
            reverse("rate_movie", args=[self.movie.pk]),
            {"score": 8.0},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_rate_movie_view_updates_average(self):
        self.client.login(username="alice", password="pass1234")
        response = self.client.post(
            reverse("rate_movie", args=[self.movie.pk]),
            {"score": 8.0},
        )
        self.assertRedirects(response, reverse("movie_list"))

        self.movie.refresh_from_db()
        self.assertEqual(self.movie.average_rating, Decimal("8.0"))

    def test_rate_movie_view_preserves_sort_and_search(self):
        self.client.login(username="alice", password="pass1234")
        response = self.client.post(
            reverse("rate_movie", args=[self.movie.pk]),
            {"score": 7.0, "q": "Inception", "sort": "-average_rating"},
        )
        self.assertRedirects(
            response,
            f"{reverse('movie_list')}?q=Inception&sort=-average_rating",
        )

    def test_movie_list_links_to_ratings_detail(self):
        self.rating_service.rate_movie(self.user, self.movie.pk, Decimal("8.0"))
        response = self.client.get(reverse("movie_list"))
        self.assertContains(response, reverse("movie_ratings", args=[self.movie.pk]))
        self.assertNotContains(response, "alice")

    def test_movie_ratings_view(self):
        self.rating_service.rate_movie(self.user, self.movie.pk, Decimal("8.0"))
        self.rating_service.rate_movie(self.other_user, self.movie.pk, Decimal("6.0"))

        response = self.client.get(reverse("movie_ratings", args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alice")
        self.assertContains(response, "bob")
        self.assertContains(response, "8.0")
        self.assertContains(response, "6.0")
        self.assertContains(response, "7.0")
        self.assertContains(response, "2 ratings")


class PatternTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="observer", password="pass")
        self.movie = MovieService().add_movie(
            title="Blade Runner",
            director="Ridley Scott",
            release_year=1982,
            genre="Sci-Fi",
        )

    def test_observer_recalculates_average(self):
        observer = AverageRatingObserver()
        observer.on_rating_changed(self.movie)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.average_rating, Decimal("0"))

        Rating.objects.create(user=self.user, movie=self.movie, score=Decimal("8.0"))
        observer.on_rating_changed(self.movie)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.average_rating, Decimal("8.0"))

    def test_rating_service_notifies_observer(self):
        RatingService(observers=[AverageRatingObserver()]).rate_movie(
            self.user, self.movie.pk, Decimal("7.5")
        )
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.average_rating, Decimal("7.5"))

    def test_genre_search_strategy(self):
        service = MovieService()
        service.add_movie(
            title="Other Film",
            director="Someone",
            release_year=2000,
            genre="Comedy",
        )
        results = service.search_movies("Sci", search_strategy="genre")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Blade Runner")

    def test_json_adapter_loads_movies(self):
        movies = JsonMovieAdapter.load_from_file()
        self.assertEqual(len(movies), 5)
        self.assertEqual(movies[0].title, "The Shawshank Redemption")

    def test_import_from_json(self):
        Movie.objects.all().delete()
        added = MovieService().import_from_json()
        self.assertEqual(added, 5)
        self.assertEqual(Movie.objects.count(), 5)
