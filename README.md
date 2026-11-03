# MovieShelf — Personal Movie Library

MovieShelf is a small, full-stack movie-library web application built with Python, Flask, SQLite, HTML, and CSS. It helps you keep track of movies you want to watch, are watching, and have watched.

## Features

- Add, view, edit, and delete movies
- Record release year, genre, personal rating, watch status, and notes
- Search movie titles
- Filter by genre and watch status
- Dashboard statistics for library size, watched movies, and average rating
- Persistent local SQLite storage
- Input validation and parameterized database queries
- Responsive dark-themed interface
- Automated tests using Python's built-in `unittest`

## Requirements

- Python 3.9 or newer
- pip

No external API key, account, or paid service is required.

## Setup

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   python app.py
   ```

6. Open the local address printed in the terminal (usually `http://127.0.0.1:5000`).

The SQLite database is created automatically in the `instance` folder the first time the application starts.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
movieshelf/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── movie_form.html
│   └── movie_detail.html
├── static/
│   └── css/
│       └── style.css
└── tests/
    └── test_app.py
```

## Security and privacy

- MovieShelf does not need API keys or third-party credentials.
- User input is passed to SQLite using parameterized queries.
- Local database files and virtual environments are excluded through `.gitignore`.
- The built-in Flask server is intended for local development. Configure a production WSGI server and appropriate security settings before deploying publicly.

## Future ideas

- Add movie poster uploads
- Import and export a library as CSV
- Add user accounts for multiple private libraries
- Add sorting by rating, year, and title

## License

MIT. See [LICENSE](LICENSE).
