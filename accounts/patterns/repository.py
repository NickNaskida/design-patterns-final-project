from abc import ABC, abstractmethod

from django.contrib.auth.models import User


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, username, password, first_name, last_name):
        pass


class DjangoUserRepository(UserRepository):
    def create_user(self, username, password, first_name="", last_name=""):
        return User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
