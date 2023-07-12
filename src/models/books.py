from datetime import datetime
from src.app import db
import uuid

class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.String(50), primary_key=True, default=lambda: uuid.uuid1().hex)
    ISBN = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    _validations_ = {
        "ISBN": {"type": "string", "required": True, "min_length": 10, "max_length": 20},
        "title": {"type": "string", "required": True, "min_length": 1, "max_length": 100},
        "author": {"type": "string", "required": True, "min_length": 1, "max_length": 100},
    }

    _restrict_in_creation_  = ["book_id", "created_at", "updated_at"]
    _restrict_in_update_    = ["book_id", "created_at", "updated_at"]