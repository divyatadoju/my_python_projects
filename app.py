"""MovieShelf: a personal movie library built with Flask and SQLite."""

import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, flash, g, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE = BASE_DIR / "instance" / "movieshelf.sqlite3"
GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Science Fiction",
    "Thriller", "Other",
]
STATUSES = ["Want to Watch", "Watching", "Watched"]


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.environ.get("MOVIESHELF_DATABASE", str(DEFAULT_DATABASE)),
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or os.urandom(32),
    )
    if test_config:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    init_db(app)

    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        search = request.args.get("q", "").strip()
        genre = request.args.get("genre", "").strip()
        status = request.args.get("status", "").strip()

        query = "SELECT * FROM movies WHERE 1=1"
        params = []
        if search:
            query += " AND title LIKE ?"
            params.append(f"%{search}%")
        if genre in GENRES:
            query += " AND genre = ?"
            params.append(genre)
        if status in STATUSES:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC, id DESC"

        movies = get_db().execute(query, params).fetchall()
        stats = get_db().execute(
            """
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN status = 'Watched' THEN 1 ELSE 0 END) AS watched,
                   ROUND(AVG(rating), 1) AS average_rating
            FROM movies
            """
        ).fetchone()
        return render_template(
            "index.html", movies=movies, genres=GENRES, statuses=STATUSES,
            search=search, selected_genre=genre, selected_status=status,
            stats=stats,
        )

    @app.route("/movie/add", methods=["GET", "POST"])
    def add_movie():
        if request.method == "POST":
            data, error = validate_movie_form()
            if error:
                flash(error, "error")
                return render_template("movie_form.html", movie=request.form, genres=GENRES, statuses=STATUSES)
            cursor = get_db().execute(
                """INSERT INTO movies (title, year, genre, rating, status, notes)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                data,
            )
            get_db().commit()
            flash("Movie added to your library.", "success")
            return redirect(url_for("movie_detail", movie_id=cursor.lastrowid))
        return render_template("movie_form.html", movie={}, genres=GENRES, statuses=STATUSES)

    @app.route("/movie/<int:movie_id>")
    def movie_detail(movie_id):
        movie = get_movie_or_404(movie_id)
        return render_template("movie_detail.html", movie=movie)

    @app.route("/movie/<int:movie_id>/edit", methods=["GET", "POST"])
    def edit_movie(movie_id):
        movie = get_movie_or_404(movie_id)
        if request.method == "POST":
            data, error = validate_movie_form()
            if error:
                flash(error, "error")
                return render_template("movie_form.html", movie=request.form, genres=GENRES, statuses=STATUSES)
            get_db().execute(
                """UPDATE movies
                   SET title=?, year=?, genre=?, rating=?, status=?, notes=?
                   WHERE id=?""",
                (*data, movie_id),
            )
            get_db().commit()
            flash("Movie details updated.", "success")
            return redirect(url_for("movie_detail", movie_id=movie_id))
        return render_template("movie_form.html", movie=movie, genres=GENRES, statuses=STATUSES)

    @app.route("/movie/<int:movie_id>/delete", methods=["POST"])
    def delete_movie(movie_id):
        get_movie_or_404(movie_id)
        get_db().execute("DELETE FROM movies WHERE id=?", (movie_id,))
        get_db().commit()
        flash("Movie removed from your library.", "success")
        return redirect(url_for("index"))

    return app


def get_db():
    if "db" not in g:
        connection = sqlite3.connect(current_app_config_database())
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


def current_app_config_database():
    from flask import current_app
    return current_app.config["DATABASE"]


def init_db(app):
    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                genre TEXT NOT NULL,
                rating REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'Want to Watch',
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.commit()
        db.close()


def get_movie_or_404(movie_id):
    movie = get_db().execute("SELECT * FROM movies WHERE id=?", (movie_id,)).fetchone()
    if movie is None:
        abort(404)
    return movie


def validate_movie_form():
    title = request.form.get("title", "").strip()
    year_text = request.form.get("year", "").strip()
    genre = request.form.get("genre", "")
    rating_text = request.form.get("rating", "0").strip()
    status = request.form.get("status", "Want to Watch")
    notes = request.form.get("notes", "").strip()

    if not title:
        return None, "Please enter a movie title."
    if len(title) > 120:
        return None, "Movie title must be 120 characters or fewer."
    try:
        year = int(year_text)
        if not 1888 <= year <= 2100:
            raise ValueError
    except ValueError:
        return None, "Enter a valid release year between 1888 and 2100."
    if genre not in GENRES:
        return None, "Please choose a valid genre."
    try:
        rating = float(rating_text)
        if not 0 <= rating <= 10:
            raise ValueError
    except ValueError:
        return None, "Rating must be between 0 and 10."
    if status not in STATUSES:
        return None, "Please choose a valid watch status."
    return (title, year, genre, rating, status, notes), None


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
