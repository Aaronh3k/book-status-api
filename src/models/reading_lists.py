from datetime import datetime
from src.app import db
import uuid

class ReadingList(db.Model):
    __tablename__ = "reading_lists"

    list_id = db.Column(db.String(50), primary_key=True, default=lambda: uuid.uuid1().hex)
    book_id = db.Column(db.String(50), db.ForeignKey("books.book_id"), nullable=False)
    # enum  for status = unread, in_progress, finished
    status  = db.Column(db.String(20),  default="unread", nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    _validations_ = {
        "book_id": {"type": "string", "required": True, "min_length": 1, "max_length": 50},
        "status":  {"type": "enum",   "required": True, "options": ["unread", "in_progress", "finished"]},
    }

    _restrict_in_creation_  = ["list_id", "created_at", "updated_at"]
    _restrict_in_update_    = ["list_id", "created_at", "updated_at"]

    book = db.relationship("Book", backref=db.backref("reading_lists", cascade="all, delete-orphan"))