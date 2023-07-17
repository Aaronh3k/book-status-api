from flask import Blueprint, request
from src.models.book_ratings import BookRating
from src.helpers import *
from src.app import app

@app.route(BASE_PATH + "/ratings", methods=["POST"])
def create_a_rating():
    """
    Create a new rating
    """
    app.logger.info('Create rating request received')

    data = request.get_json()
    app.logger.debug(f'Request data: {data}')

    result = BookRating.create_a_rating(data)

    if result.get("error"):
        app.logger.error('Rating creation failed')
        app.logger.debug(f'Error details: {result}')
        return errorit(result, "RATING_CREATION_FAILED", 400)
    else:
        app.logger.info('Rating successfully created')
        return responsify(result, {}, 201)

@app.route(BASE_PATH + "/ratings/<rating_id>", methods=["GET"])
def get_a_rating(rating_id):
    """
    Get a rating's information

    :param rating_id: [str] book_ratings table primary key
    """
    app.logger.info(f'Rating information request received for Rating ID: {rating_id}')

    rating = BookRating.get_ratings(rating_id)

    if not rating:
        app.logger.error(f'Rating not found for ID: {rating_id}')
        return errorit("No such rating found", "RATING_NOT_FOUND", 404)
    else:
        app.logger.info(f'Rating information retrieved for ID: {rating_id}')
        return responsify(rating, {})

@app.route(BASE_PATH + "/ratings", methods=["GET"])
def get_ratings():
    """
    Get many ratings' information
    """
    app.logger.info('Get ratings request received')

    sorting_column = None
    orderby = None

    if request.args.get("orderby") and request.args.get("sortby"):
        if request.args.get("orderby") == "1":
            orderby = 1
        elif request.args.get("orderby") == "-1":
            orderby = -1
        else:
            app.logger.warning('Invalid orderby value')
            return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be rating or createdAt"}, "TAG_ERROR", 400)

        if request.args.get("sortby") == "rating":
            sorting_column = "rating"
        elif request.args.get("sortby") == "createdAt":
            sorting_column = "created_at"
        else:
            app.logger.warning('Invalid sortby value')
            return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be rating or createdAt"}, "TAG_ERROR", 400)

    app.logger.debug(f'Orderby: {orderby}, Sorting column: {sorting_column}')

    ratings = BookRating.get_ratings(None, False, request.args.get("page_number"), request.args.get("page_offset"), orderby, sorting_column)

    if not ratings:
        app.logger.info('No ratings found')
        return responsify({"ratings":[]}, {})
    elif type(ratings) is dict:
        app.logger.info('Single rating found')
        return responsify(ratings, {}, 200)
    else:
        app.logger.info(f'{len(ratings)} ratings found')
        return responsify(ratings, {})

@app.route(BASE_PATH + "/ratings/<rating_id>", methods=["PATCH"])
def update_a_rating(rating_id):
    """
    Update rating information

    :param rating_id: [str] book_ratings table primary key
    """
    app.logger.info(f'Update rating request received for rating id: {rating_id}')

    data = request.get_json()
    app.logger.debug(f'Request data: {data}')

    result = BookRating.update_a_rating(rating_id, data)

    if not result:
        app.logger.error(f'No rating found for id: {rating_id}')
        return {"error": "No such rating found", "status": 404}, 404
    elif result.get("error"):
        app.logger.error('Rating update failed')
        app.logger.debug(f'Error details: {result.get("error")}')
        return {"error": result.get("error"), "status": 400}, 400
    else:
        app.logger.info(f'Rating successfully updated for id: {rating_id}')
        return responsify(result, {}, 200)

@app.route(BASE_PATH + "/ratings/<rating_id>", methods=["DELETE"])
def delete_rating_permanently(rating_id):
    """
    Delete a rating permanently

    :param rating_id: [str] book_ratings table primary key
    """
    app.logger.info(f'Delete rating request received for rating_id: {rating_id}')

    result = BookRating.delete_rating_permanently(rating_id)

    if not result:
        app.logger.warning(f'No rating found for rating_id: {rating_id}')
        return errorit("No such rating found", "RATING_NOT_FOUND", 404)

    if result.get("error"):
        app.logger.error('Rating deletion failed')
        app.logger.debug(f'Error details: {result}')
        return errorit(result, "RATING_DELETION_FAILED", 400)

    app.logger.info('Rating successfully deleted')
    return responsify(result, {}, 200)