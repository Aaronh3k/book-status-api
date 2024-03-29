from datetime import datetime
from src.app import db, app
import uuid
from src.models.mixins import BaseMixin
from src.helpers import *
from sqlalchemy import exc

class ReadingList(BaseMixin, db.Model):
    __tablename__ = "reading_lists"

    list_id = db.Column(db.String(50), primary_key=True, default=lambda: uuid.uuid1().hex)
    book_id = db.Column(db.String(50), db.ForeignKey("books.book_id"), nullable=False, unique=True)
    # enum  for status = unread, in_progress, finished
    status  = db.Column(db.String(20),  default="unread", nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    _validations_ = {
        "book_id": {"type": "string", "required": True, "min_length": 32, "max_length": 32},
        "status":  {"type": "enum",   "required": True, "options": ["unread", "in_progress", "finished"]},
    }

    _restrict_in_creation_  = ["list_id", "created_at", "updated_at"]
    _restrict_in_update_    = ["list_id", "book_id", "created_at", "updated_at"]

    book = db.relationship("Book", backref=db.backref("reading_lists", cascade="all, delete-orphan"))

    
    @staticmethod
    def create_a_reading_list(data):
        """
        Create a new reading list
        :param data: [object] contains reading list info in key value pair

        :return [dict]
        """
        app.logger.info('Create reading list request received')
        app.logger.debug(f'Request data: {data}')
        
        new_reading_list = ReadingList()
        allowed_columns = list_diff(ReadingList().columns_list(), ReadingList()._restrict_in_creation_)

        for column in allowed_columns:
            if column in data:
                setattr(new_reading_list, column, data.get(column))

        # Check if data is valid
        result  = new_reading_list.validate_and_sanitize(ReadingList()._restrict_in_creation_)
        if result.get("errors"):
            app.logger.error('Reading list creation failed during validation')
            app.logger.debug(f'Error details: {result["errors"]}')
            return {"error": result["errors"]}

        try:
            db.session.add(new_reading_list)
            db.session.flush()
            db.session.commit()
            app.logger.info('Reading list successfully created')
            return {"list_id": str(new_reading_list.list_id)}
        except exc.IntegrityError as e:
            db.session.rollback()
            err = e.orig.diag.message_detail.rsplit(',', 1)[-1]
            app.logger.error('Reading list creation failed due to Integrity Error')
            app.logger.debug(f'Error details: {err.replace(")", "")}')
            return {"error": err.replace(")", "")}
        except Exception as e:
            db.session.rollback()
            app.logger.error('Reading list creation failed due to Exception')
            app.logger.debug(f'Error details: {str(e)}')
            return {"error": "failed to create reading list"}
    
    @staticmethod
    def get_reading_lists(list_id=None, return_as_object=False, page=None, offset=None, orderby=None, sortby=None, status=None):
        """
        Get reading lists info

        :param list_id: [str] reading_lists table primary key
        :param return_as_object: [bool] do we need to return the list of objects or dictionary for rows?
        :param page: [int] page number
        :param offset: [int] page offset - number of rows to return

        :return [list]
        """

        app.logger.info('Get reading list request received')
        app.logger.debug(f'Request params: list_id={list_id}, return_as_object={return_as_object}, page={page}, offset={offset}, orderby={orderby}, sortby={sortby}, status={status}')
        
        page =  page or 1
        offset =  offset or 20
        begin_query = db.session.query(ReadingList)
    
        try:
            if not list_id:
                offset = int(offset)
                page = int(page)-1
                
                if status:
                    begin_query = begin_query.filter(ReadingList.status == status)
                
                if orderby and sortby:
                    if orderby == -1:
                        result = begin_query.order_by(getattr(ReadingList, sortby).desc()).offset(page*offset).limit(offset).all()
                    elif orderby == 1:
                        result = begin_query.order_by(getattr(ReadingList, sortby).asc()).offset(page*offset).limit(offset).all()
                else:
                    result = begin_query.order_by(ReadingList.created_at).offset(page*offset).limit(offset).all()

                count = ReadingList.query.count()
                meta_data = {"reading_list_count": count, "page_number": int(page) + 1, "page_offset": offset}
    
                if result:
                    if return_as_object:
                        return result
                    else:
                        return {"reading_lists": [row.to_dict() for row in result], **meta_data}

            else:
                result = begin_query.filter(
                    ReadingList.list_id == list_id
                    ).all()
                if result:
                    return result[0] if return_as_object else result[0].to_dict()

        except Exception as e:
            app.logger.error('Getting reading list failed')
            app.logger.debug(f'Error details: {str(e)}, list_id={list_id}, page={page}, offset={offset}')
            return {"error" : "No reading list found"}
    
    @staticmethod
    def update_a_reading_list(list_id, data):
        """
        Update an existing reading list

        :param list_id: [str] reading_list table primary key
        :param data: [dict] reading_list updating field data

        :return [dict]
        """
        app.logger.info(f'Update reading list request received for list_id: {list_id}')
        app.logger.debug(f'Request data: {data}')

        reading_list = db.session.get(ReadingList, list_id)
        if not reading_list:
            app.logger.error('Reading list not found')
            return {}

        try:
            for column in data:
                if hasattr(reading_list, column):
                    setattr(reading_list, column, data[column])
            reading_list.updated_at = datetime.utcnow()
            db.session.commit()
            app.logger.info('Reading list successfully updated')
            return {'message': 'successfully updated list_id={}'.format(list_id)}
        except Exception as e:
            db.session.rollback()
            app.logger.error('Reading list update failed due to Exception')
            app.logger.debug(f'Error details: {str(e)}')
            return {"error": "failed to update reading list"}
    
    @staticmethod
    def delete_reading_list_permanently(list_id):
        """
        Delete a reading list permanently

        :param list_id: [str] reading_list table primary key

        :return [dict]
        """
        app.logger.info(f'Delete reading list request received for list_id: {list_id}')

        reading_list = ReadingList.get_reading_lists(list_id, True)

        if reading_list:
            try:
                db.session.delete(reading_list)
                db.session.commit()
                app.logger.info('Reading list successfully deleted')
                return {"action": "deleted successfully"}
            except Exception as e:
                db.session.rollback()
                app.logger.error('Reading list deletion failed')
                app.logger.debug(f'Error details: {str(e)}')
                return {"error": "Reading list deletion failed"}
        else:
            app.logger.warning(f'No reading list found with list_id: {list_id}')
            return {}