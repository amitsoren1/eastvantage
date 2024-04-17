import asyncio
import unittest
from fastapi.testclient import TestClient
from tests.database_for_test import create_all, drop_all, app

app_client = TestClient(app)

class TestBookAPI(unittest.TestCase):
    def setUp(self):
        asyncio.run(create_all())

    def tearDown(self):
        asyncio.run(drop_all())

    def test_create_book_invalid_request(self):
        book_payload = {
            "title": "string",
            "author": "string",
            "publication_year": 0
        }
        res = app_client.post("/book", json=book_payload)
        self.assertEqual(res.status_code, 422)

    def test_create_book_valid_request(self):
        book_payload = {
            "title": "book name",
            "author": "book author",
            "publication_year": 2024
        }
        res = app_client.post("/book", json=book_payload)
        self.assertEqual(res.status_code, 201)

    def test_list_books(self):
        book_payload = {
            "title": "book name 1",
            "author": "book author 1",
            "publication_year": 1000
        }
        app_client.post("/book", json=book_payload)
        book_payload = {
            "title": "book name 2",
            "author": "book author 2",
            "publication_year": 2024
        }
        app_client.post("/book", json=book_payload)

        res = app_client.get("/book")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 2)

    def test_list_books_with_filter(self):
        book_payload = {
            "title": "book name 1",
            "author": "book author 1",
            "publication_year": 1000
        }
        app_client.post("/book", json=book_payload)
        book_payload = {
            "title": "book name 2",
            "author": "book author 2",
            "publication_year": 2024
        }
        app_client.post("/book", json=book_payload)

        res = app_client.get("/book?author=book author 2&publish_year=2024")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["author"], "book author 2")

        res = app_client.get("/book?author=no book author&publish_year=1")
        self.assertEqual(len(res.json()), 0)


if __name__ == '__main__':
    unittest.main()
