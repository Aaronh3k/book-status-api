from flask import Blueprint, request
from src.models.books import Book
from src.helpers import *
from src.app import app

@app.route(BASE_PATH + "/books", methods=["POST"])
def create_a_book():
    """
    Create a new book
    """
    result = Book.create_a_book(request.get_json())
    if result.get("error"):
        return errorit(result, "BOOK_CREATION_FAILED", 400)
    else:
        return responsify(result, {}, 201)

@app.route(BASE_PATH + "/books/<book_id>", methods=["GET"])
def get_a_book(book_id):
  """
  Get a book's information

  :param book_id: [str] books table primary key
  """
  book = Book.get_books(book_id)

  if not book:
    return errorit("No such book found", "BOOK_NOT_FOUND", 404)
  else:
    return responsify(book, {})

@app.route(BASE_PATH + "/books", methods=["GET"])
def get_books():
  """
  Get many books' information
  """

  sorting_column = None
  orderby = None

  if request.args.get("orderby") and request.args.get("sortby"):
    if request.args.get("orderby") == "1":
      orderby = 1
    elif request.args.get("orderby") == "-1":
      orderby = -1
    else:
      return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be book title or createdAt"}, "TAG_ERROR", 400)
    if request.args.get("sortby") == "title":
      sorting_column = "title"
    elif request.args.get("sortby") == "createdAt":
      sorting_column = "created_at"
    else:
      return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be book title or createdAt"}, "TAG_ERROR", 400)
  
  books = Book.get_books(None, False, request.args.get("page_number"), request.args.get("page_offset"), orderby, sorting_column)
  if not books:
    return responsify({"books":[]}, {})
  elif type(books) is dict:
    return responsify(books, {}, 200)
  else:
    return responsify(books, {})

@app.route(BASE_PATH + "/books/<book_id>", methods=["PATCH"])
def update_a_book(book_id):
    """
    Update book information

    :param book_id: [str] books table primary key
    """
    result = Book.update_a_book(book_id, request.get_json())

    if not result:
        return {"error": "No such book found", "status": 404}, 404
    elif result.get("error"):
        return {"error": result.get("error"), "status": 400}, 400
    else:
        return result, 200
    
@app.route(BASE_PATH + "/books/<book_id>", methods=["DELETE"])
def delete_book_permanently(book_id):
  """
  Delete a book permanently

  :param book_id: [str] books table primary key
  """
  result = Book.delete_book_permanently(book_id)
  if not result:
    return errorit("No such book found", "BOOK_NOT_FOUND", 404)
  if result.get("error"):
    return errorit(result, "BOOK_DELETION_FAILED", 400)
  return responsify(result, {}, 200)
