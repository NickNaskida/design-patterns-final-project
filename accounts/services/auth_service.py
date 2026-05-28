from accounts.patterns.repository import DjangoUserRepository


class AuthService:
    def __init__(self, repo=None):
        self.repo = repo or DjangoUserRepository()

    def register(self, username, password, first_name, last_name):
        return self.repo.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
