from unittest import TestCase
import pytest
import json
from src.models.reading_lists import ReadingList
from src.models.books import Book

class TestReadingListOperations(TestCase):
    @pytest.fixture(autouse=True)
    def setup_class(self, app, db):
        self.app = app
        self.db = db

        # First, create a book
        self.new_book = Book(ISBN="1234567890123", title="Test Book", author="Test Author")
        self.db.session.add(self.new_book)
        self.db.session.commit()

        self.new_reading_list = {
            "book_id": self.new_book.book_id,
            "status": "unread"
        }
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()
    
    def test_create_a_reading_list(self):
        response = self.app.test_client().post(
            "v1/readinglists",
            data=json.dumps(self.new_reading_list),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.new_reading_list["list_id"] = json.loads(response.data)['list_id']

    def test_get_a_reading_list(self):
        self.test_create_a_reading_list()
        response = self.app.test_client().get(f"v1/reading_lists/{self.new_reading_list['list_id']}")
        self.assertEqual(response.status_code, 200)

    def test_update_a_reading_list(self):
        self.test_create_a_reading_list()
        updated_data = {"status": "in_progress"}
        response = self.app.test_client().patch(
            f"v1/reading_lists/{self.new_reading_list['list_id']}",
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], f"successfully updated list_id={self.new_reading_list['list_id']}")

    def test_delete_reading_list_permanently(self):
        self.test_create_a_reading_list()
        response = self.app.test_client().delete(f"v1/reading_lists/{self.new_reading_list['list_id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['action'], "deleted successfully")

    def test_get_reading_lists(self):
        self.test_create_a_reading_list()
        response = self.app.test_client().get("v1/reading_lists")
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_reading_list(self):
        response = self.app.test_client().get("v1/reading_lists/non_existent_list_id")
        self.assertEqual(response.status_code, 404)

    def test_delete_non_existent_reading_list(self):
        response = self.app.test_client().delete("v1/reading_lists/non_existent_list_id")
        self.assertEqual(response.status_code, 404)

    def test_create_invalid_reading_list(self):
        invalid_reading_list = {"status": "unknown_status"}
        response = self.app.test_client().post(
            "v1/readinglists",
            data=json.dumps(invalid_reading_list),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def tearDown(self):
        with self.app_context:
            self.db.session.rollback()
            # Check if "list_id" key exists in the dictionary
            if "list_id" in self.new_reading_list:
                reading_list = ReadingList.query.filter_by(list_id=self.new_reading_list["list_id"]).first()
                if reading_list:
                    self.db.session.delete(reading_list)
                    self.db.session.commit()
            # Also delete the book that was created
            book = Book.query.filter_by(ISBN=self.new_book.ISBN).first()  # Query the book from the database first
            if book:
                self.db.session.delete(book)
                self.db.session.commit()
        self.app_context.pop()