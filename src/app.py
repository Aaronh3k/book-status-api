from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.helpers import *
from src.config import config
import os

app = Flask("book_status_api")
# Load config to app
app.config.from_pyfile("src/config/config.py")

db = SQLAlchemy(app, session_options={"autocommit": True, "autoflush": False})

@app.route("/", methods=["GET", "OPTIONS"])
def root_uri():
    return responsify({"message": "Hello World. Welcome to Book Status Service API.", "version": "0.0.1"})

# Handle all error cases
@app.errorhandler(404)
def error_400(error):
  return errorit("No such endpoint found", "UNKNOWN_ENDPOINT", 404)

@app.errorhandler(405)
def error_405(error):
  return errorit("The method is not allowed for the requested URL", "METHOD_NOT_ALLOWED", 405)

@app.errorhandler(500)
def error_500(error):
  return errorit("The server encountered an internal error and was unable to complete your request.", "INTERNAL_SERVER_ERROR", 500)