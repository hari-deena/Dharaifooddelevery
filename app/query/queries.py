# from sqlalchemy import text
# from typing import Type, Dict, Any, Optional
# from typing import List, Type, Optional
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.declarative import DeclarativeMeta
# from sqlalchemy.orm.attributes import InstrumentedAttribute
# from ..core.logger_config import configure_logger
# logger = configure_logger('justplay')

# # Fetches the first record from the specified model that matches the given filters.
# def get_first_record(
#     db: Session,
#     model: Type[DeclarativeMeta],
#     filters: List,
# ) -> Optional[object]:
#     try:
#         return db.query(model).filter(*filters).first()
#     except Exception as e:
#         logger.error(f"Unexpected error in get_first_record: {e}", exc_info=True)
#         return False

# # Retrieves specific fields from records in a model that match the provided filters.
# def get_filtered_fields(
#     db: Session,
#     model: Type[DeclarativeMeta],
#     field: List[InstrumentedAttribute],
#     filters: List
# ):
#     try:
#         return db.query(*field).filter(*filters).all()
#     except Exception as e:
#         logger.error(f"Unexpected error in get_filtered_fields: {e}", exc_info=True)
#         return False

# # Creates and inserts a new record into the database from the provided data and returns the inserted object.
# def insert_record(
#     db: Session,
#     model: Type[DeclarativeMeta],
#     data: Dict[str, Any]
# ) -> Optional[object]:
    
#     try:
#         new_record = model(**data)
#         db.add(new_record)
#         db.commit()
#         db.refresh(new_record)
#         return new_record
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Failed to insert record into {model.__name__}: {e}", exc_info=True)
#         return None
    
# # Updates records in the database that match the filter condition with the provided data 
# # and returns the number of rows updated.
# def update_records(
#     db: Session,
#     model: Type[DeclarativeMeta],
#     filter_condition: Any,
#     update_data: Dict[str, Any]
# ) -> int:
#     try:
#         result = db.query(model).filter(filter_condition).update(
#             update_data, synchronize_session=False
#         )
#         db.commit()
#         return result if result else None
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Failed to update {model.__name__}: {e}", exc_info=True)
#         return None