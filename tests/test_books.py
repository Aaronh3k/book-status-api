from unittest import TestCase
import pytest
import json

from src.models.books import Book

class TestBookOperations(TestCase):
    @pytest.fixture(autouse=True)
    def setup_class(self, app, db):
        self.app = app
        self.db = db

        self.new_book = {
            "ISBN": "9783161484100",
            "title": "Some Title",
            "author": "Some Author"
        }
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()

    def test_get_book(self):
        # Create a book first
        response = self.app.test_client().post(
            "/v1/books",
            data=json.dumps(self.new_book),
            content_type='application/json'
        )
        book_id = json.loads(response.data)['book_id']

        # Now try to get it
        response = self.app.test_client().get(f"/v1/books/{book_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['title'], self.new_book['title'])

    def test_update_book(self):
        # Create a book first
        response = self.app.test_client().post(
            "/v1/books",
            data=json.dumps(self.new_book),
            content_type='application/json'
        )
        book_id = json.loads(response.data)['book_id']

        # Update the created book
        updated_data = {"title": "Updated Title", "author": "Updated Author"}
        response = self.app.test_client().patch(
            f"/v1/books/{book_id}",
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], f"successfully updated book_id={book_id}")

    def test_delete_book(self):
        # Create a book first
        response = self.app.test_client().post(
            "/v1/books",
            data=json.dumps(self.new_book),
            content_type='application/json'
        )
        book_id = json.loads(response.data)['book_id']

        # Delete the created book
        response = self.app.test_client().delete(f"/v1/books/{book_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['action'], "deleted successfully")

    def tearDown(self):
        with self.app_context:
            self.db.session.rollback()
            book = Book.query.filter_by(ISBN=self.new_book["ISBN"]).first()
            if book:
                self.db.session.delete(book)
                self.db.session.commit()
        self.app_context.pop()