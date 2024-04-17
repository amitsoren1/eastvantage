import asyncio
import unittest
from fastapi.testclient import TestClient
from tests.database_for_test import create_all, drop_all, app

app_client = TestClient(app)

def create_a_book(name="book name"):
    review_payload = {
            "title": name,
            "author": "book author",
            "publication_year": 2024
        }
    res = app_client.post("/book", json=review_payload)
    return res.json()["id"]

class TestBookAPI(unittest.TestCase):
    def setUp(self):
        asyncio.run(create_all())
        self.book_id = create_a_book()

    def tearDown(self):
        asyncio.run(drop_all())

    def test_submit_review_invalid_request(self):
        review_payload = {
            "book_id": "string",
            "review_text": "string",
            "rating": 1000
        }
        res = app_client.post("/review", json=review_payload)
        self.assertEqual(res.status_code, 422)

    def test_submit_review_valid_request(self):
        review_payload = {
            "book_id": self.book_id,
            "review_text": "good book",
            "rating": 8
        }
        res = app_client.post("/review", json=review_payload)
        self.assertEqual(res.status_code, 201)

    def test_list_reviews(self):
        review_payload = {
            "book_id": self.book_id,
            "review_text": "good book 1",
            "rating": 8
        }
        app_client.post("/review", json=review_payload)
        review_payload = {
            "book_id": create_a_book("book name 2"),
            "review_text": "good book 2",
            "rating": 7
        }
        app_client.post("/review", json=review_payload)

        res = app_client.get("/review")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 2)


if __name__ == '__main__':
    unittest.main()
