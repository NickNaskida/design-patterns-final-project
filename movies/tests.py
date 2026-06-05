from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from movies.models import Movie
from movies.services.movie_service import MovieService

class MovieTests(TestCase):
    def setUp(self):
        self.service = MovieService()
        self.movie = self.service.add_movie(
            title="Inception",
            director="Christopher Nolan",
            release_year=2010,
            genre="Sci-Fi",
            average_rating=Decimal("8.8")
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
        response = self.client.get(reverse('edit_movie', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('edit_movie', args=[self.movie.pk]), {
            'title': 'Inception Edited',
            'director': 'Christopher Nolan',
            'release_year': 2010,
            'genre': 'Sci-Fi',
            'average_rating': 9.0
        })
        self.assertRedirects(response, reverse('movie_list'))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, 'Inception Edited')

    def test_delete_movie_view(self):
        response = self.client.get(reverse('delete_movie', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('delete_movie', args=[self.movie.pk]))
        self.assertRedirects(response, reverse('movie_list'))
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())

    def test_search_movies_service(self):
        self.service.add_movie(title="The Dark Knight", director="Christopher Nolan", release_year=2008, genre="Action", average_rating=9.0)
        results = self.service.search_movies("Inception")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Inception")
        
        results = self.service.search_movies("Nolan")
        self.assertEqual(len(results), 2)

    def test_search_movies_view(self):
        self.service.add_movie(title="The Dark Knight", director="Christopher Nolan", release_year=2008, genre="Action", average_rating=9.0)
        response = self.client.get(reverse('movie_list'), {'q': 'Dark'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Dark Knight")
        self.assertNotContains(response, "Inception")

    def test_rating_validation(self):
        from django.core.exceptions import ValidationError
        from movies.forms import MovieForm
        
        # Test valid rating
        form = MovieForm(data={
            'title': 'Test Movie',
            'director': 'Test Director',
            'release_year': 2022,
            'genre': 'Drama',
            'average_rating': 5.5
        })
        self.assertTrue(form.is_valid())
        
        # Test rating too high
        form = MovieForm(data={
            'title': 'Test Movie',
            'director': 'Test Director',
            'release_year': 2022,
            'genre': 'Drama',
            'average_rating': 11.0
        })
        self.assertFalse(form.is_valid())
        self.assertIn('average_rating', form.errors)
        
        # Test rating too low
        form = MovieForm(data={
            'title': 'Test Movie',
            'director': 'Test Director',
            'release_year': 2022,
            'genre': 'Drama',
            'average_rating': -1.0
        })
        self.assertFalse(form.is_valid())
        self.assertIn('average_rating', form.errors)

    def test_service_rating_validation(self):
        from django.core.exceptions import ValidationError
        
        # Test service layer enforcement
        with self.assertRaises(ValidationError):
            self.service.add_movie(
                title='Test Movie',
                director='Test Director',
                release_year=2022,
                genre='Drama',
                average_rating=15.0  # Invalid
            )



