# Movie Ratings

Django app for a design patterns course project. Stores movies in SQLite and lists them on a simple HTML page.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/setup_database.py
python manage.py runserver
```

App: http://127.0.0.1:8000/

The setup script runs migrations and loads sample movies. To reset the database:

```bash
rm db.sqlite3
python scripts/setup_database.py
```

## Commands

| Command | Description |
|---------|-------------|
| `python scripts/setup_database.py` | Migrate and seed |
| `python manage.py migrate` | Apply migrations |
| `python manage.py makemigrations` | Create migrations after model changes |
| `python manage.py seed_movies` | Seed only (skips if movies exist) |
| `python manage.py runserver` | Dev server |

## Layout

```
movieratings/     project settings and urls
movies/
  models.py
  migrations/   0001_initial.py (Movie)
  views.py
  patterns/       repository, factory
  services/       movie_service
  templates/
  management/commands/seed_movies.py
scripts/setup_database.py
```

## Patterns

- **MVT** — `Movie` model, `movie_list` view, HTML template
- **Repository** — `movies/patterns/repository.py` (`MovieRepository`, `DjangoMovieRepository`)
- **Factory** — `movies/patterns/factory.py` (`MovieDataFactory` for seed data)
- **Service layer** — `movies/services/movie_service.py` used by views and seed command

## References

- [Django docs](https://docs.djangoproject.com/en/stable/)
- [SQLite](https://www.sqlite.org/docs.html)
