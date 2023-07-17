from flask import Blueprint, request
from src.models.books import Book
from src.helpers import *
from src.app import app
import boto3
import json

@app.route(BASE_PATH + "/books", methods=["POST"])
def create_a_book():
    """
    Create a new book
    """
    app.logger.info('Create book request received')

    data = request.get_json()
    app.logger.debug(f'Request data: {data}')
    
    result = Book.create_a_book(data)

    if result.get("error"):
        app.logger.error('Book creation failed')
        app.logger.debug(f'Error details: {result}')
        return errorit(result, "BOOK_CREATION_FAILED", 400)
    else:
        app.logger.info('Book successfully created')
        return responsify(result, {}, 201)


@app.route(BASE_PATH + "/books/<book_id>", methods=["GET"])
def get_a_book(book_id):
    """
    Get a book's information

    :param book_id: [str] books table primary key
    """
    app.logger.info(f'Book information request received for Book ID: {book_id}')

    book = Book.get_books(book_id)

    if not book:
        app.logger.error(f'Book not found for ID: {book_id}')
        return errorit("No such book found", "BOOK_NOT_FOUND", 404)
    else:
        app.logger.info(f'Book information retrieved for ID: {book_id}')
        return responsify(book, {})

@app.route(BASE_PATH + "/books", methods=["GET"])
def get_books():
    """
    Get many books' information
    """
    app.logger.info('Get books request received')

    sorting_column = None
    orderby = None

    if request.args.get("orderby") and request.args.get("sortby"):
        if request.args.get("orderby") == "1":
            orderby = 1
        elif request.args.get("orderby") == "-1":
            orderby = -1
        else:
            app.logger.warning('Invalid orderby value')
            return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be book title or createdAt"}, "TAG_ERROR", 400)

        if request.args.get("sortby") == "title":
            sorting_column = "title"
        elif request.args.get("sortby") == "createdAt":
            sorting_column = "created_at"
        else:
            app.logger.warning('Invalid sortby value')
            return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be book title or createdAt"}, "TAG_ERROR", 400)

    app.logger.debug(f'Orderby: {orderby}, Sorting column: {sorting_column}')

    books = Book.get_books(None, False, request.args.get("page_number"), request.args.get("page_offset"), orderby, sorting_column)
    
    if not books:
        app.logger.info('No books found')
        return responsify({"books":[]}, {})
    elif type(books) is dict:
        app.logger.info('Single book found')
        return responsify(books, {}, 200)
    else:
        app.logger.info(f'{len(books)} books found')
        return responsify(books, {})

@app.route(BASE_PATH + "/books/<book_id>", methods=["PATCH"])
def update_a_book(book_id):
    """
    Update book information

    :param book_id: [str] books table primary key
    """
    app.logger.info(f'Update book request received for book id: {book_id}')

    data = request.get_json()
    app.logger.debug(f'Request data: {data}')
    
    result = Book.update_a_book(book_id, data)

    if not result:
        app.logger.error(f'No book found for id: {book_id}')
        return {"error": "No such book found", "status": 404}, 404
    elif result.get("error"):
        app.logger.error('Book update failed')
        app.logger.debug(f'Error details: {result.get("error")}')
        return {"error": result.get("error"), "status": 400}, 400
    else:
        app.logger.info(f'Book successfully updated for id: {book_id}')
        return result, 200
    
@app.route(BASE_PATH + "/books/<book_id>", methods=["DELETE"])
def delete_book_permanently(book_id):
  """
  Delete a book permanently

  :param book_id: [str] books table primary key
  """
  app.logger.info(f'Delete book request received for book_id: {book_id}')

  result = Book.delete_book_permanently(book_id)

  if not result:
    app.logger.warning(f'No book found for book_id: {book_id}')
    return errorit("No such book found", "BOOK_NOT_FOUND", 404)

  if result.get("error"):
    app.logger.error('Book deletion failed')
    app.logger.debug(f'Error details: {result}')
    return errorit(result, "BOOK_DELETION_FAILED", 400)

  app.logger.info('Book successfully deleted')
  return responsify(result, {}, 200)

@app.route(BASE_PATH + "/books/isbn/<isbn>", methods=["GET"])
def get_book_by_isbn(isbn):
    """
    Get a book's information by ISBN

    :param isbn: [str] Book's ISBN
    """
    app.logger.info(f'Book information request received for ISBN: {isbn}')

    book = Book.get_book_by_isbn(isbn)

    if not book:
        app.logger.error(f'Book not found for ISBN: {isbn}')
        return errorit("No such book found", "BOOK_NOT_FOUND", 404)
    else:
        app.logger.info(f'Book information retrieved for ISBN: {isbn}')
        return responsify(book, {})

@app.route(BASE_PATH + '/books/upload', methods=['POST'])
def upload_books():
    """
    Upload books using Google Books API

    :param number_of_books: [int] Number of books to be uploaded
    """
    app.logger.info(f'Book upload request received. Request to upload {request.json.get("number_of_books")} books.')
    
    # Create SQS client
    sqs = boto3.client('sqs', region_name='us-east-1')
    number_of_books = request.json.get('number_of_books')
    keyword = request.json.get('keyword')

    # Send message to SQS queue
    sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps({'number_of_books': number_of_books, 'keyword': keyword}))

    # Log information about the sent message
    app.logger.info(f'Message sent to SQS. Request to upload {number_of_books} books.')

    return responsify({"message": "Book upload request received"}, {}, 202)