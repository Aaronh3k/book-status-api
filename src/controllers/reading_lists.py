from src.models.reading_lists import ReadingList
from src.helpers import *
from src.app import app
from flask import request

@app.route(BASE_PATH + "/readinglists", methods=["POST"])
def create_a_reading_list():
    """
    Create a new reading list
    """
    app.logger.info('Create reading list request received')

    data = request.get_json()
    app.logger.debug(f'Request data: {data}')
    
    result = ReadingList.create_a_reading_list(data)

    if result.get("error"):
        app.logger.error('Reading list creation failed')
        app.logger.debug(f'Error details: {result}')
        return errorit(result, "READINGLIST_CREATION_FAILED", 400)
    else:
        app.logger.info('Reading list successfully created')
        return responsify(result, {}, 201)

@app.route(BASE_PATH + "/reading_lists/<list_id>", methods=["GET"])
def get_a_reading_list(list_id):
    """
    Get a reading list's information

    :param list_id: [str] reading_lists table primary key
    """
    app.logger.info(f'Get reading list request received for list_id: {list_id}')

    reading_list = ReadingList.get_reading_lists(list_id)

    if not reading_list:
        app.logger.warning(f'No reading list found for list_id: {list_id}')
        return errorit("No such reading list found", "READING_LIST_NOT_FOUND", 404)
    else:
        app.logger.info(f'Reading list successfully retrieved for list_id: {list_id}')
        return responsify(reading_list, {})

@app.route(BASE_PATH + "/reading_lists", methods=["GET"])
def get_reading_lists():
    """
    Get many reading lists' information
    """
    app.logger.info('Get reading lists request received')

    sorting_column = None
    orderby = None

    if request.args.get("orderby") and request.args.get("sortby"):
        if request.args.get("orderby") == "1":
            orderby = 1
        elif request.args.get("orderby") == "-1":
            orderby = -1
        else:
            app.logger.error('Invalid orderby value received')
            return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be createdAt"}, "TAG_ERROR", 400)
        
        if request.args.get("sortby") == "createdAt":
            sorting_column = "created_at"
        else:
            app.logger.error('Invalid sortby value received')
            return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be createdAt"}, "TAG_ERROR", 400)
    
    if request.args.get("status") and request.args.get("status") not in ["unread", "in_progress", "finished"]:
        app.logger.error('Invalid status value received')
        return errorit({"statusy":"should be either unread, in_progress, or finished"}, "TAG_ERROR", 400)
        
    app.logger.debug('Fetching reading lists from database')
    reading_lists = ReadingList.get_reading_lists(None, False, request.args.get("page_number"), request.args.get("page_offset"), orderby, sorting_column, request.args.get("status"))
    
    if not reading_lists:
        app.logger.info('No reading lists found')
        return responsify({"reading_lists":[]}, {})
    elif type(reading_lists) is dict:
        app.logger.info('Reading lists found and returned')
        return responsify(reading_lists, {}, 200)
    else:
        app.logger.error('Unexpected result type when getting reading lists')
        return responsify(reading_lists, {})
    
@app.route(BASE_PATH + "/reading_lists/<list_id>", methods=["PATCH"])
def update_a_reading_list(list_id):
    """
    Update reading list information

    :param list_id: [str] reading_list table primary key
    """
    app.logger.info(f'Update reading list request received for list_id: {list_id}')

    data = request.get_json()
    app.logger.debug(f'Request data: {data}')

    result = ReadingList.update_a_reading_list(list_id, data)

    if not result:
        app.logger.warning(f'No such reading list found for list_id: {list_id}')
        return {"error": "No such reading list found", "status": 404}, 404
    elif result.get("error"):
        app.logger.error('Failed to update reading list')
        app.logger.debug(f'Error details: {result.get("error")}')
        return {"error": result.get("error"), "status": 400}, 400
    else:
        app.logger.info(f'Reading list successfully updated for list_id: {list_id}')
        return result, 200

@app.route(BASE_PATH + "/reading_lists/<list_id>", methods=["DELETE"])
def delete_reading_list_permanently(list_id):
    """
    Delete a reading list permanently

    :param list_id: [str] reading_list table primary key
    """
    app.logger.info(f'Delete reading list request received for list id: {list_id}')

    result = ReadingList.delete_reading_list_permanently(list_id)
    
    if not result:
        app.logger.error(f'No such reading list found for list id: {list_id}')
        return errorit("No such reading list found", "READING_LIST_NOT_FOUND", 404)
    if result.get("error"):
        app.logger.error('Reading list deletion failed')
        app.logger.debug(f'Error details: {result}')
        return errorit(result, "READING_LIST_DELETION_FAILED", 400)
    
    app.logger.info(f'Reading list successfully deleted for list id: {list_id}')
    return responsify(result, {}, 200)