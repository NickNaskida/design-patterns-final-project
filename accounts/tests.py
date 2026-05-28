from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationFlowTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "ada",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "password1": "Sup3rSecret!42",
                "password2": "Sup3rSecret!42",
            },
        )

        self.assertRedirects(response, reverse("movie_list"))
        user = User.objects.get(username="ada")
        self.assertEqual(user.get_full_name(), "Ada Lovelace")
        self.assertTrue(user.check_password("Sup3rSecret!42"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_movie_list_shows_full_name_when_logged_in(self):
        User.objects.create_user(
            username="ada",
            password="Sup3rSecret!42",
            first_name="Ada",
            last_name="Lovelace",
        )
        self.client.login(username="ada", password="Sup3rSecret!42")

        response = self.client.get(reverse("movie_list"))

        self.assertContains(response, "Ada Lovelace")
        self.assertNotContains(response, 'href="{}"'.format(reverse("login")))

    def test_movie_list_shows_auth_links_when_anonymous(self):
        response = self.client.get(reverse("movie_list"))

        self.assertContains(response, reverse("login"))
        self.assertContains(response, reverse("register"))


class LoginLogoutTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="ada",
            password="Sup3rSecret!42",
            first_name="Ada",
            last_name="Lovelace",
        )

    def test_login_redirects_to_movie_list(self):
        response = self.client.post(
            reverse("login"),
            {"username": "ada", "password": "Sup3rSecret!42"},
        )
        self.assertRedirects(response, reverse("movie_list"))

    def test_logout_requires_post_and_redirects(self):
        self.client.login(username="ada", password="Sup3rSecret!42")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("movie_list"))
        self.assertNotIn("_auth_user_id", self.client.session)
