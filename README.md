# Movie Ratings

Django app for a design patterns course project. Stores movies in SQLite and lists them on a simple HTML page.

## What you need first

- **Python 3.10 or newer** (3.12 is fine)
- A terminal (Terminal on Mac, PowerShell or Command Prompt on Windows)
- This project folder on your machine

Check Python:

```bash
python3 --version
```

If that fails on Windows, try:

```bash
py --version
```

---

## Project setup (step by step)

Do everything from the **project root** — the folder that contains `manage.py`.

### 1. Open the project folder

```bash
cd path/to/design-patterns-final-project
```

Replace `path/to/` with wherever you cloned or unzipped the repo.

### 2. Create a virtual environment

This keeps project packages separate from the rest of your system.

**Mac / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt or PowerShell):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` at the start of your terminal line. That means the venv is active.

If you close the terminal later, run the `activate` command again before working on the project.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Wait until it finishes without errors.

### 4. Create the database and sample data

```bash
python scripts/setup_database.py
```

This does two things:

1. **Migrations** — creates `db.sqlite3` and the tables Django needs (including `Movie`)
2. **Seed** — adds five sample movies

You should see migration output, then something like `added 5 movies`.

If you already have movies in the database, you might see `nothing to add (db not empty?)` instead. That is normal.

**Manual alternative** (same result):

```bash
python manage.py migrate
python manage.py seed_movies
```

### 5. Start the server

```bash
python manage.py runserver
```

Leave this terminal window open while you use the app.

Open a browser and go to:

**http://127.0.0.1:8000/**

You should see a table of movies (title, director, year, genre, rating).

To stop the server: press `Ctrl+C` in that terminal.

---

## Starting over (fresh database)

If something is broken or you want empty tables again:

```bash
rm db.sqlite3
python scripts/setup_database.py
python manage.py runserver
```

On Windows PowerShell:

```powershell
Remove-Item db.sqlite3
python scripts/setup_database.py
python manage.py runserver
```

---

## Common problems

| Problem | What to try |
|---------|-------------|
| `python3: command not found` | Use `python` instead of `python3` |
| `No module named django` | Activate `.venv`, then run `pip install -r requirements.txt` again |
| Port already in use | Run `python manage.py runserver 8001` and open http://127.0.0.1:8001/ |
| Page shows no movies | Run `python manage.py seed_movies` or `python scripts/setup_database.py` |
| Changed `models.py` | Run `python manage.py makemigrations` then `python manage.py migrate` |

---

## Commands

| Command | Description |
|---------|-------------|
| `python scripts/setup_database.py` | Migrate and seed (easiest first-time setup) |
| `python manage.py migrate` | Apply migrations only |
| `python manage.py makemigrations` | Create new migration files after model changes |
| `python manage.py seed_movies` | Add sample movies (skips if DB already has movies) |
| `python manage.py runserver` | Start the dev server |
| `python manage.py createsuperuser` | Optional — for Django admin at `/admin/` |

---

## Layout

```
movieratings/     project settings and urls
movies/
  models.py
  migrations/     0001_initial.py (Movie)
  views.py
  patterns/       repository, factory
  services/       movie_service
  templates/
  management/commands/seed_movies.py
scripts/setup_database.py
```

---

## Patterns

- **MVT** — `Movie` model, `movie_list` view, HTML template
- **Repository** — `movies/patterns/repository.py` (`MovieRepository`, `DjangoMovieRepository`)
- **Factory** — `movies/patterns/factory.py` (`MovieDataFactory` for seed data)
- **Service layer** — `movies/services/movie_service.py` used by views and seed command

---

## References

- [Django docs](https://docs.djangoproject.com/en/stable/)
- [SQLite](https://www.sqlite.org/docs.html)
