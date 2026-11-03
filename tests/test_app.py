import tempfile
import unittest
from pathlib import Path

from app import create_app


class MovieShelfTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database = str(Path(self.temp_dir.name) / "test.sqlite3")
        self.app = create_app({"TESTING": True, "DATABASE": database})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def add_movie(self, **overrides):
        data = {
            "title": "Spirited Away",
            "year": "2001",
            "genre": "Animation",
            "rating": "9.5",
            "status": "Watched",
            "notes": "A wonderful film.",
        }
        data.update(overrides)
        return self.client.post("/movie/add", data=data, follow_redirects=True)

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MovieShelf", response.data)

    def test_add_movie(self):
        response = self.add_movie()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Spirited Away", response.data)

    def test_reject_empty_title(self):
        response = self.add_movie(title=" ")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter a movie title", response.data)

    def test_search_movie(self):
        self.add_movie()
        response = self.client.get("/?q=Spirited")
        self.assertIn(b"Spirited Away", response.data)
        response = self.client.get("/?q=Inception")
        self.assertNotIn(b"Spirited Away", response.data)

    def test_edit_movie(self):
        self.add_movie()
        response = self.client.post(
            "/movie/1/edit",
            data={"title": "Spirited Away Updated", "year": "2001",
                  "genre": "Animation", "rating": "10", "status": "Watched",
                  "notes": "Updated note"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Spirited Away Updated", response.data)

    def test_delete_movie(self):
        self.add_movie()
        response = self.client.post("/movie/1/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Spirited Away", response.data)

    def test_invalid_movie_id_returns_404(self):
        self.assertEqual(self.client.get("/movie/999").status_code, 404)


if __name__ == "__main__":
    unittest.main()
