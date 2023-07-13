from datetime import datetime
from src.app import db
import uuid
from src.models.mixins import BaseMixin
from src.helpers import *
from sqlalchemy import exc

class Book(BaseMixin, db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.String(50), primary_key=True, default=lambda: uuid.uuid1().hex)
    ISBN = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    _validations_ = {
        "ISBN": {"type": "string", "required": True, "min_length": 10, "max_length": 13},
        "title": {"type": "string", "required": True, "min_length": 1, "max_length": 100},
        "author": {"type": "string", "required": True, "min_length": 1, "max_length": 100},
    }

    _restrict_in_creation_  = ["book_id", "created_at", "updated_at"]
    _restrict_in_update_    = ["book_id", "created_at", "updated_at"]
    
    
    @staticmethod
    def create_a_book(data):
        """
        Create a new book
        :param data: [object] contains book info in key value pair

        :return [dict]
        """
        new_book = Book()
        allowed_columns = list_diff(Book().columns_list(), Book()._restrict_in_creation_)

        for column in allowed_columns:
          if column in data:
            setattr(new_book, column, data.get(column))

        # Check if data is valid
        result  = new_book.validate_and_sanitize(Book()._restrict_in_creation_)
        if result.get("errors"):
          return {"error": result["errors"]}

        try:
          db.session.add(new_book)
          db.session.flush()
          db.session.commit()
          return {"book_id": str(new_book.book_id)}
        except exc.IntegrityError as e:
          db.session.rollback()
          err = e.orig.diag.message_detail.rsplit(',', 1)[-1]
          return {"error": err.replace(")", "")}
        except Exception as e:
          db.session.rollback()
          return {"error": "failed to create book"}
    
    
    @staticmethod
    def get_books(book_id=None, return_as_object=False, page=None, offset=None, orderby=None, sortby=None):
        """
        Get books info

        :param book_id: [str] books table primary key
        :param return_as_object: [bool] do we need to return the list of objects or dictionary for rows?
        :param page: [int] page number
        :param offset: [int] page offset - number of rows to return

        :return [list]
        """

        page =  page or 1
        offset =  offset or 20
        begin_query = db.session.query(Book)
        try:
            if not book_id:
                offset = int(offset)
                page = int(page)-1

                if orderby and sortby:
                    if orderby == -1:
                        result = begin_query.order_by(getattr(Book, sortby).desc()).offset(page*offset).limit(offset).all()
                    elif orderby == 1:
                        result = begin_query.order_by(getattr(Book, sortby).asc()).offset(page*offset).limit(offset).all()
                else:
                    result = begin_query.order_by(Book.title).offset(page*offset).limit(offset).all()

                count = Book.query.count()
                meta_data = {"book_count": count, "page_number": int(page) + 1, "page_offset": offset}
                if result:
                    if return_as_object:
                        return result
                    else:
                        return {"books": [row.to_dict() for row in result], **meta_data}

            else:
                result = begin_query.filter(
                    Book.book_id == book_id
                    ).all()
                if result:
                    return result[0] if return_as_object else result[0].to_dict()

        except Exception as e:
            print("ACTION=GETTING_BOOK_FAILED. error={}, book_id={}, page={}, offset={}".format(e, book_id, page, offset))
            return {"error" : "No book found"}
    
    
    @staticmethod
    def update_a_book(book_id, data):
        """
        Update an existing book

        :param book_id: [str] books table primary key
        :param data: [dict] book updating field data

        :return [dict]
        """
        book = Book.query.get(book_id)
        if not book:
            return {}

        try:
            for column in data:
                if hasattr(book, column):
                    setattr(book, column, data[column])
            book.updated_at = datetime.utcnow()
            db.session.commit()
            return {'message': 'successfully updated book_id={}'.format(book_id)}
        except Exception as e:
            return {"error": "failed to update book"}
    
    
    @staticmethod
    def delete_book_permanently(book_id):
        """
        Delete a book permanently

        :param book_id: [str] books table primary key

        :return [dict]
        """
        book = Book.get_books(book_id, True)

        if book:
          try:
            db.session.delete(book)
            db.session.commit()
            return {"action": "deleted successfully"}
          except Exception as e:
            print(e)
            return {"error": "Book deletion failed"}
        else:
          return {}
