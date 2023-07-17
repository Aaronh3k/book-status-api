from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.helpers import *
from src.config import config
import os
import logging
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask("book_status_api", static_url_path='/static')

# Load config to app
app.config.from_pyfile("src/config/config.py")
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI

# StreamHandler for logging
stream_handler = logging.StreamHandler()

# Set the log level to INFO
stream_handler.setLevel(logging.INFO)

# format logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# Adding the handler to app's logger
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)

# Swagger UI setup
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yml'  # Path to YAML file

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be served at '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Book Status Service API"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

db = SQLAlchemy(app)

# wires up controller routes
import src.controllers

@app.route("/v1/", methods=["GET", "OPTIONS"])
def root_uri():
    app.logger.info('Root URI accessed')
    return responsify({"message": "Hello World. Welcome to Book Status Service API.", "version": "0.0.1"})

# Handle all error cases
@app.errorhandler(404)
def error_404(error):
  app.logger.error('404 error occurred')
  return errorit("No such endpoint found", "UNKNOWN_ENDPOINT", 404)

@app.errorhandler(405)
def error_405(error):
  app.logger.error('405 error occurred')
  return errorit("The method is not allowed for the requested URL", "METHOD_NOT_ALLOWED", 405)

@app.errorhandler(500)
def error_500(error):
  app.logger.error('500 error occurred')
  return errorit("The server encountered an internal error and was unable to complete your request.", "INTERNAL_SERVER_ERROR", 500)