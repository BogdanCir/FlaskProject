import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import unittest
from app import create_app
from app.db import Base, engine, db_session
from app.anagram import anagrams, calculate_key


class UnitTest(unittest.TestCase):
    # unit tests
    def test_basic_grouping(self):
        result = anagrams(["ana", "naa", "ban", "nab"])
        self.assertIn(["ana", "naa"], result)
        self.assertIn(["ban", "nab"], result)

    def test_single_word(self):
        self.assertEqual(anagrams(["hello"]), [["hello"]])

    def test_empty_list(self):
        self.assertEqual(anagrams([]), [])

    def test_key_ignores_order(self):
        self.assertEqual(
            calculate_key(["ban", "ana"]),
            calculate_key(["ana", "ban"])
        )


class IntegrationTest(unittest.TestCase):
    # integration test
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
        with self.app.app_context():
            Base.metadata.create_all(bind=engine)

    def tearDown(self):
        with self.app.app_context():
            Base.metadata.drop_all(bind=engine)
            db_session.remove()

    def test_new_list_returns_201(self):
        response = self.client.post("/api/anagrams", json={"words": ["ana", "naa"]})
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.get_json()["seen"])

    def test_duplicate_returns_cache(self):
        self.client.post("/api/anagrams", json={"words": ["ana", "naa"]})
        response = self.client.post("/api/anagrams", json={"words": ["ana", "naa"]})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["seen"])

    def test_different_order_returns_cache(self):
        self.client.post("/api/anagrams", json={"words": ["ana", "naa"]})
        response = self.client.post("/api/anagrams", json={"words": ["naa", "ana"]})
        self.assertTrue(response.get_json()["seen"])

    def test_history_empty(self):
        response = self.client.get("/api/history")
        self.assertEqual(response.get_json(), [])

    def test_history_returns_results(self):
        self.client.post("/api/anagrams", json={"words": ["ana", "naa"]})
        response = self.client.get("/api/history")
        self.assertEqual(len(response.get_json()), 1)


if __name__ == "__main__":
    unittest.main()