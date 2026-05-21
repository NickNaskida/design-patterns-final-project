# Movie Ratings — Design Patterns Final Project

A minimal Django web application for a movie rating system. This repository is the foundation for a design-patterns course project: it demonstrates several classic patterns in a small, readable codebase while keeping the UI intentionally plain (HTML only, no CSS framework).

## Current scope (Phase 1)

- **Movie** model stored in **SQLite**
- Sample data seeded via management command
- Simple HTML page listing all movies at `/`
- Explicit design patterns: **Repository**, **Factory**, plus Django’s **MVT**

Planned later phases (not implemented yet): user accounts, per-user ratings, reviews, and additional patterns (e.g. Observer, Strategy).

---

## Requirements

- Python 3.10+ (developed with Python 3.12)
- pip

## Quick start

```bash
# From the project root
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# One command: create DB tables + seed sample movies
python scripts/setup_database.py

python manage.py runserver
```

On macOS/Linux you can also run the shell wrapper (auto-uses `.venv` if it exists):

```bash
chmod +x scripts/setup_database.sh   # first time only
./scripts/setup_database.sh
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the movie list.

Optional admin (create a superuser first):

```bash
python manage.py createsuperuser
python manage.py runserver
# http://127.0.0.1:8000/admin/
```

---

## Project structure

```
design-patterns-final-project/
├── manage.py                 # Django CLI entry point
├── requirements.txt          # Python dependencies
├── scripts/
│   ├── setup_database.py     # Migrate + seed (recommended for new clones)
│   └── setup_database.sh     # Shell wrapper (Unix)
├── db.sqlite3                # SQLite database (created after setup script)
├── README.md                 # This file
├── scratch/                  # Non-production notes & presentation context
│   └── PROJECT_CONTEXT.md
├── movieratings/             # Django project package (settings, URLs)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── movies/                   # Main application
    ├── models.py             # Movie model
    ├── views.py              # MVT view — movie list
    ├── urls.py               # App URL routing
    ├── admin.py              # Django admin registration
    ├── templates/
    │   └── movies/
    │       └── movie_list.html
    ├── patterns/             # Design pattern implementations
    │   ├── repository.py     # Repository (abstract + Django ORM)
    │   └── factory.py        # Factory — sample movie creation
    ├── services/
    │   └── movie_service.py  # Service layer / orchestration
    └── management/
        └── commands/
            └── seed_movies.py
```

---

## Design patterns in this codebase

| Pattern | Location | Role |
|--------|----------|------|
| **MVT (Model–View–Template)** | Django core + `movies/views.py`, `movie_list.html` | Web request handling and rendering |
| **Repository** | `movies/patterns/repository.py` | Hides persistence; views/services use `MovieRepository` instead of raw ORM |
| **Factory** | `movies/patterns/factory.py` | Builds `Movie` instances from a catalog of seed data |
| **Service / Facade** | `movies/services/movie_service.py` | Coordinates repository + factory for list and seed operations |

### Request flow (movie list)

```
Browser → urls.py → movie_list view → MovieService
    → DjangoMovieRepository
    → Movie.objects (ORM) → SQLite
    → template movie_list.html
```

### Seeding flow

```
python manage.py seed_movies → MovieService.seed_sample_data()
    → MovieDataFactory.create_all_samples() (Factory)
    → DjangoMovieRepository.save() (Repository)
```

---

## Movie model

| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField | Movie title |
| `director` | CharField | Director name |
| `release_year` | PositiveIntegerField | Year released |
| `genre` | CharField | Genre label |
| `average_rating` | DecimalField | Placeholder aggregate rating (future user ratings) |

---

## Database setup script

Use this after cloning or whenever you need a fresh local database with sample movies.

| Script | What it does |
|--------|----------------|
| `python scripts/setup_database.py` | Runs `migrate` then `seed_movies` |
| `./scripts/setup_database.sh` | Same; prefers `.venv/bin/python` on Unix |

**Steps performed:**

1. **`migrate`** — creates/updates `db.sqlite3` and all Django tables (including `movies_movie`).
2. **`seed_movies`** — inserts five sample movies via `MovieDataFactory` + `MovieService` (skipped if movies already exist).

**Equivalent manual commands:**

```bash
python manage.py migrate
python manage.py seed_movies
```

**Re-seed from scratch:** delete `db.sqlite3`, then run the setup script again.

```bash
rm -f db.sqlite3
python scripts/setup_database.py
```

---

## Management commands

| Command | Description |
|---------|-------------|
| `python scripts/setup_database.py` | **Recommended** — migrate + seed in one step |
| `python manage.py migrate` | Apply database migrations only |
| `python manage.py seed_movies` | Insert sample movies only (skips if DB already has movies) |
| `python manage.py runserver` | Start development server |

---

## Configuration

- **Database:** SQLite at `db.sqlite3` (see `movieratings/settings.py` → `DATABASES`)
- **Debug:** `DEBUG = True` (development only)
- **Installed app:** `movies` registered in `INSTALLED_APPS`

---

## Official documentation

- [Django documentation](https://docs.djangoproject.com/en/stable/)
- [Django models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django templates](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Django management commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/)
- [SQLite](https://www.sqlite.org/docs.html)
- [Python venv](https://docs.python.org/3/library/venv.html)

Design patterns (general reference, not framework-specific):

- [Refactoring Guru — Design Patterns](https://refactoring.guru/design-patterns)

---

## Development notes

- No CSS or static assets by design for Phase 1.
- `.venv/` and `db.sqlite3` are gitignored; recreate locally with the quick start steps.
- Presentation / AI context for current progress: see `scratch/PROJECT_CONTEXT.md`.

---

## License

Course project — use per your institution’s guidelines.
