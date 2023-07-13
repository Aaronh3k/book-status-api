from src.models.reading_lists import ReadingList
from src.helpers import *
from src.app import app
from flask import request

@app.route(BASE_PATH + "/readinglists", methods=["POST"])
def create_a_reading_list():
    """
    Create a new reading list
    """
    result = ReadingList.create_a_reading_list(request.get_json())
    if result.get("error"):
        return errorit(result, "READINGLIST_CREATION_FAILED", 400)
    else:
        return responsify(result, {}, 201)


@app.route(BASE_PATH + "/reading_lists/<list_id>", methods=["GET"])
def get_a_reading_list(list_id):
    """
    Get a reading list's information

    :param list_id: [str] reading_lists table primary key
    """
    reading_list = ReadingList.get_reading_lists(list_id)

    if not reading_list:
        return errorit("No such reading list found", "READING_LIST_NOT_FOUND", 404)
    else:
        return responsify(reading_list, {})

@app.route(BASE_PATH + "/reading_lists", methods=["GET"])
def get_reading_lists():
    """
    Get many reading lists' information
    """

    sorting_column = None
    orderby = None

    if request.args.get("orderby") and request.args.get("sortby"):
        if request.args.get("orderby") == "1":
            orderby = 1
        elif request.args.get("orderby") == "-1":
            orderby = -1
        else:
            return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be createdAt"}, "TAG_ERROR", 400)
        
        if request.args.get("sortby") == "createdAt":
            sorting_column = "created_at"
        else:
            return errorit({"orderby":"should be 1 for ascending or -1 for descending","sortby":"should be createdAt"}, "TAG_ERROR", 400)
    
    if request.args.get("status") and request.args.get("status") not in ["unread", "in_progress", "finished"]:
        return errorit({"statusy":"should be either unread, in_progress, or finished"}, "TAG_ERROR", 400)
        
    
    reading_lists = ReadingList.get_reading_lists(None, False, request.args.get("page_number"), request.args.get("page_offset"), orderby, sorting_column, request.args.get("status"))
    
    if not reading_lists:
        return responsify({"reading_lists":[]}, {})
    elif type(reading_lists) is dict:
        return responsify(reading_lists, {}, 200)
    else:
        return responsify(reading_lists, {})
    
@app.route(BASE_PATH + "/reading_lists/<list_id>", methods=["PATCH"])
def update_a_reading_list(list_id):
    """
    Update reading list information

    :param list_id: [str] reading_list table primary key
    """
    result = ReadingList.update_a_reading_list(list_id, request.get_json())

    if not result:
        return {"error": "No such reading list found", "status": 404}, 404
    elif result.get("error"):
        return {"error": result.get("error"), "status": 400}, 400
    else:
        return result, 200

@app.route(BASE_PATH + "/reading_lists/<list_id>", methods=["DELETE"])
def delete_reading_list_permanently(list_id):
    """
    Delete a reading list permanently

    :param list_id: [str] reading_list table primary key
    """
    result = ReadingList.delete_reading_list_permanently(list_id)
    if not result:
        return errorit("No such reading list found", "READING_LIST_NOT_FOUND", 404)
    if result.get("error"):
        return errorit(result, "READING_LIST_DELETION_FAILED", 400)
    return responsify(result, {}, 200)

