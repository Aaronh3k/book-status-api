from unittest import TestCase
import pytest
import json

from src.models.book_ratings import BookRating
from src.models.books import Book
from src.models.reading_lists import ReadingList

class TestBookRatingOperations(TestCase):
    @pytest.fixture(autouse=True)
    def setup_class(self, app, db):
        self.app = app
        self.db = db

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()

    def setUp(self):
        self.book_data = {
            "ISBN": "9783161484100",
            "title": "Book Title",
            "author": "Book Author"
        }
        self.reading_list_data = {
            "status": "unread"
        }
        self.new_book = Book.create_a_book(self.book_data)
        self.new_reading_list = ReadingList.create_a_reading_list({**self.reading_list_data, "book_id": self.new_book["book_id"]})

        self.new_rating = {
            "book_id": self.new_book["book_id"],
            "list_id": self.new_reading_list["list_id"],
            "rating": 4,
            "notes": "Great Book!"
        }
        self.rating_id = None
    
    def test_create_rating(self):
        response = self.app.test_client().post(
            "/v1/ratings",
            data=json.dumps(self.new_rating),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.rating_id = json.loads(response.data)['rating_id']
        self.assertIsNotNone(self.rating_id)

    def test_get_rating(self):
        self.test_create_rating()  # Create a rating first
        response = self.app.test_client().get(f"/v1/ratings/{self.rating_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['rating'], self.new_rating['rating'])

    def test_update_rating(self):
        self.test_create_rating()  # Create a rating first
        updated_data = {"rating": 5}
        response = self.app.test_client().patch(
            f"/v1/ratings/{self.rating_id}",
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], f"successfully updated rating_id={self.rating_id}")

    def test_delete_rating(self):
        self.test_create_rating()  # Create a rating first
        response = self.app.test_client().delete(f"/v1/ratings/{self.rating_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], f"successfully deleted rating_id={self.rating_id}")
 
    def test_get_ratings(self):
        response = self.app.test_client().get("/v1/ratings")
        self.assertEqual(response.status_code, 200)
        self.assertIn('ratings', json.loads(response.data))
        self.assertGreaterEqual(len(json.loads(response.data)['ratings']), 0)

    def tearDown(self):
        with self.app_context:
            self.db.session.rollback()
            if self.rating_id:
                rating = BookRating.query.filter_by(rating_id=self.rating_id).first()
                if rating:
                    self.db.session.delete(rating)
                    self.db.session.commit()
            book = Book.query.filter_by(book_id=self.new_book["book_id"]).first()
            if book:
                self.db.session.delete(book)
                self.db.session.commit()
            reading_list = ReadingList.query.filter_by(list_id=self.new_reading_list["list_id"]).first()
            if reading_list:
                self.db.session.delete(reading_list)
                self.db.session.commit()
        self.app_context.pop()