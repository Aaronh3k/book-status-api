from datetime import datetime
from src.app import db, app
import uuid
from src.models.mixins import BaseMixin
from src.helpers import *
from sqlalchemy import exc

class BookRating(BaseMixin, db.Model):
    __tablename__ = "book_ratings"

    rating_id = db.Column(db.String(50), primary_key=True, default=lambda: uuid.uuid1().hex)
    book_id = db.Column(db.String(50), db.ForeignKey("books.book_id"), nullable=False)
    list_id = db.Column(db.String(50), db.ForeignKey("reading_lists.list_id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(500))
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    _validations_ = {
        "book_id": {"type": "string", "required": True, "min_length": 32, "max_length": 32},
        "list_id": {"type": "string", "required": True, "min_length": 32, "max_length": 32},
        "rating": {"type": "integer", "required": True, "min_value": 0, "max_value": 5},
        "notes": {"type": "string", "required": False, "min_length": 0, "max_length": 500},
    }

    _restrict_in_creation_  = ["rating_id", "created_at", "updated_at"]
    _restrict_in_update_    = ["rating_id", "created_at", "book_id", "list_id"]

    __table_args__ = (db.UniqueConstraint('book_id', 'list_id', name='uq_book_list'),)

    @staticmethod
    def create_a_rating(data):
        """
        Create a new rating
        :param data: [object] contains rating info in key value pair

        :return [dict]
        """
        app.logger.info('Preparing to create a new rating')

        new_rating = BookRating()
        allowed_columns = list_diff(BookRating().columns_list(), BookRating()._restrict_in_creation_)

        for column in allowed_columns:
            if column in data:
                setattr(new_rating, column, data.get(column))

        app.logger.debug('Populated new rating object with provided data')

        # Check if data is valid
        result = new_rating.validate_and_sanitize(BookRating()._restrict_in_creation_)
        if result.get("errors"):
            app.logger.error('Validation and sanitization failed for new rating')
            app.logger.debug(f'Error details: {result["errors"]}')
            return {"error": result["errors"]}

        try:
            db.session.add(new_rating)
            db.session.flush()
            db.session.commit()
            app.logger.info(f'New rating created successfully with id {new_rating.rating_id}')
            return {"rating_id": str(new_rating.rating_id)}
        except exc.IntegrityError as e:
            db.session.rollback()
            err = e.orig.diag.message_detail.rsplit(',', 1)[-1]
            app.logger.error('Integrity error occurred while creating new rating')
            app.logger.debug(f'Error details: {err.replace(")", "")}')
            return {"error": err.replace(")", "")}
        except Exception as e:
            db.session.rollback()
            app.logger.error('Unknown error occurred while creating new rating')
            app.logger.debug(f'Error details: {str(e)}')
            return {"error": "failed to create rating"}

    @staticmethod
    def get_ratings(rating_id=None, return_as_object=False, page=None, offset=None, orderby=None, sortby=None):
        """
        Get ratings info

        :param rating_id: [str] book_ratings table primary key
        :param return_as_object: [bool] do we need to return the list of objects or dictionary for rows?
        :param page: [int] page number
        :param offset: [int] page offset - number of rows to return

        :return [list]
        """

        page =  page or 1
        offset =  offset or 20
        begin_query = db.session.query(BookRating)

        app.logger.info('Book rating retrieval request received')
        app.logger.debug(f'Request parameters - rating_id: {rating_id}, return_as_object: {return_as_object}, page: {page}, offset: {offset}, orderby: {orderby}, sortby: {sortby}')

        try:
            if not rating_id:
                offset = int(offset)
                page = int(page)-1

                if orderby and sortby:
                    if orderby == -1:
                        result = begin_query.order_by(getattr(BookRating, sortby).desc()).offset(page*offset).limit(offset).all()
                    elif orderby == 1:
                        result = begin_query.order_by(getattr(BookRating, sortby).asc()).offset(page*offset).limit(offset).all()
                else:
                    result = begin_query.order_by(BookRating.created_at).offset(page*offset).limit(offset).all()

                count = BookRating.query.count()
                meta_data = {"rating_count": count, "page_number": int(page) + 1, "page_offset": offset}

                app.logger.info(f'Retrieved {count} ratings')

                if result:
                    if return_as_object:
                        return result
                    else:
                        return {"ratings": [row.to_dict() for row in result], **meta_data}

            else:
                result = begin_query.filter(
                    BookRating.rating_id == rating_id
                    ).all()

                if result:
                    app.logger.info(f'Retrieved rating with rating_id {rating_id}')
                    return result[0] if return_as_object else result[0].to_dict()

        except Exception as e:
            app.logger.error('Book rating retrieval failed')
            app.logger.debug(f'Error details: {e}, rating_id: {rating_id}, page: {page}, offset: {offset}')
            return {"error" : "No rating found"}

    @staticmethod
    def update_a_rating(rating_id, data):
        """
        Update an existing rating

        :param rating_id: [str] book_ratings table primary key
        :param data: [dict] rating updating field data

        :return [dict]
        """
        app.logger.info(f'Update rating request received for rating id: {rating_id}')

        app.logger.debug(f'Request data: {data}')
    
        rating = db.session.get(BookRating, rating_id) 
        if not rating:
            app.logger.error(f'No rating found with id: {rating_id}')
            return {}

        try:
            for column in data:
                if hasattr(rating, column):
                    setattr(rating, column, data[column])
            rating.updated_at = datetime.utcnow()
            db.session.commit()
            app.logger.info('Rating successfully updated')
            return {'message': 'successfully updated rating_id={}'.format(rating_id)}
        except Exception as e:
            app.logger.error('Rating update failed')
            app.logger.debug(f'Error details: {str(e)}')
            return {"error": "failed to update rating"}

    @staticmethod
    def delete_rating_permanently(rating_id):
        """
        Delete a rating permanently

        :param rating_id: [str] book_ratings table primary key

        :return [dict]
        """
        app.logger.info(f'Request to delete rating with id {rating_id} received')

        rating = db.session.get(BookRating, rating_id) 

        if rating:
            try:
                db.session.delete(rating)
                db.session.commit()
                app.logger.info('Rating successfully deleted')
                return {'message': 'successfully deleted rating_id={}'.format(rating_id)}
            except Exception as e:
                app.logger.error('Rating deletion failed')
                app.logger.debug(f'Error details: {e}')
                return {"error": "Rating deletion failed"}
        else:
            app.logger.warning(f'Rating with id {rating_id} not found')
            return {}