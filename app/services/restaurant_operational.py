from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
# from app.query.notification import get_notifications_by_customer,get_notifications_by_turf, fcm_token_field_names
# from app.query.queries import get_filtered_fields, get_first_record, insert_record, update_records
# from app.utils.email_templates import generate_booking_confirmation, generate_booking_cancellation, generate_turf_inactive_cancellation, generate_booking_completed, generate_turf_booking_confirmation_nad_cancelation
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import Restaurant, RestaurantOperationalDetails
from app.core.logger_config import configure_logger
from app.utils import config
import asyncio
from app.utils import config
from ..utils.common import create_jwt_token
from sqlalchemy import update
from uuid import uuid4
logger = configure_logger('justplay')



async def add_operational_restaurant(restaurant_operational_data, user_data, db):
    try:
        logger.info("restaurant_operational_data: -------------> %s",restaurant_operational_data)
        logger.info("user_data: -------------> %s",user_data)
        
        existing_restaurant = db.query(Restaurant).filter(
        Restaurant.restaurant_id == restaurant_operational_data.restaurant_id
        ).first()

        if not existing_restaurant:
            logger.error("Restaurant ID not found")
            return bad_request_response("Invalid restaurant id.")
        
        if restaurant_operational_data.operational_id is not None:
            # Try to find existing record
            db_record = db.query(RestaurantOperationalDetails).filter(
                RestaurantOperationalDetails.operational_id == restaurant_operational_data.operational_id
            ).first()

            if not db_record:
                return bad_request_response(f"Operational detail with ID {restaurant_operational_data.operational_id} not found")  # Or HTTPException in FastAPI

            # Update fields — only update what's provided (non-None)
            update_data = restaurant_operational_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                if hasattr(db_record, key) and value is not None:
                    setattr(db_record, key, value)
                    
            msg = "Restaurant Operational updated successfully."
            
        else:
            existing_restaurant = db.query(RestaurantOperationalDetails).filter(
            RestaurantOperationalDetails.restaurant_id == restaurant_operational_data.restaurant_id
            ).first()

            if existing_restaurant:
                logger.error("Restaurant already have operational data.")
                return bad_request_response("Restaurant already have operational data.")
        
            # Create new record
            db_record = RestaurantOperationalDetails(**restaurant_operational_data.dict(exclude_unset=True))
            db.add(db_record)
            
            msg = "Restaurant Operational added successfully."

        db.commit()
        db.refresh(db_record)
        
        logger.info("Restaurant Operational add or updated successfully.")
        return handle_success(msg)
    except Exception as e:
        logger.exception("Database error while adding restaurant: %s", str(e))
        return server_error_response("Internal server error.")   



# async def update_is_open(operational_id, restaurant_operational_data, user_data, db):
#     try:
#         logger.info("operational_id: ----------------> %s",operational_id)
#         logger.info("restaurant_operational_data: -------------> %s",restaurant_operational_data)
#         logger.info("user_data: -------------> %s",user_data)
        
#         existing_restaurant = db.query(RestaurantOperationalDetails).filter(
#         RestaurantOperationalDetails.operational_id == operational_id ).first()

#         if not existing_restaurant:
#             logger.error("Operational ID not found")
#             return bad_request_response("Invalid Operational id.")
        
        
        
#         logger.info("Update the restrunt open status.")
#         return handle_success("Update the restrunt open status.")
#     except Exception as e:
#         logger.exception("Database error while adding restaurant: %s", str(e))
#         return server_error_response("Internal server error.")   


async def update_is_open(operational_id, restaurant_operational_data, user_data, db):
    try:
        logger.info("operational_id: ----------------> %s", operational_id)
        logger.info("restaurant_operational_data: -------------> %s", restaurant_operational_data)
        logger.info("user_data: -------------> %s", user_data)

        # Fetch existing record
        existing_restaurant = db.query(RestaurantOperationalDetails).filter(
            RestaurantOperationalDetails.operational_id == operational_id
        ).first()

        if not existing_restaurant:
            logger.error("Operational ID not found")
            return bad_request_response("Invalid Operational id.")

        # Update is_open field
        existing_restaurant.is_open = restaurant_operational_data.is_open

        # Commit the transaction
        db.commit()
        db.refresh(existing_restaurant)  # Optional: to get updated instance

        logger.info("Updated restaurant open status to: %s", existing_restaurant.is_open)
        return handle_success("Restaurant open status updated successfully.")

    except Exception as e:
        logger.exception("Database error while updating restaurant open status: %s", str(e))
        db.rollback()  # Important: rollback on error
        return server_error_response("Internal server error.")



def restaurant_operational_to_dict(obj: RestaurantOperationalDetails) -> dict:
    return {
        "operational_id": obj.operational_id,
        "restaurant_id": obj.restaurant_id,
        "estimated_delivery_time": obj.estimated_delivery_time,
        "delivery_charges_per_km": obj.delivery_charges_per_km,
        "opening_time": str(obj.opening_time),
        "closing_time": str(obj.closing_time),
        "is_open": obj.is_open,
    }



# Get Restrunt operational 

# async def get_restaurant_operational(operational_id, user_data, db):
#     try:
#         logger.info("Restaurant id: %s", operational_id)
#         logger.info("User data: %s", user_data)

#         if operational_id:
#             restaurant_opration_detail = db.query(RestaurantOperationalDetails).filter(
#                 RestaurantOperationalDetails.operational_id == operational_id
#             ).first()
            
#             logger.info("restaurant_opration_detail: -----------> %s",restaurant_opration_detail)

#             if not restaurant_opration_detail:
#                 logger.error("Restaurant not found")
#                 return bad_request_response("Restaurant not found")

          
#             return handle_success("Get Successfully restrunt operational.")
            
            

#         restaurant_opration_detail = db.query(RestaurantOperationalDetails).all()
#         logger.info("Restaurants fetched successfully: %s",restaurant_opration_detail)
        
        
#         return handle_success("Get Successfully restrunt operational.")
            
#         # return handle_success_with_data(
#         #     "Successfully fetched restaurants.",
#         #     [restaurant_to_dict(r) for r in restaurants]
#         # )

#     except Exception as e:
#         logger.exception("Database error while fetching restaurant: %s", str(e))
#         return server_error_response("Internal server error.")




async def get_restaurant_operational(operational_id, user_data, db):
    try:
        logger.info("Restaurant id: %s", operational_id)
        logger.info("User data: %s", user_data)

        if operational_id:
            restaurant_opration_detail = db.query(RestaurantOperationalDetails).filter(
                RestaurantOperationalDetails.operational_id == operational_id
            ).first()
            
            logger.info("restaurant_opration_detail: -----------> %s", restaurant_opration_detail)

            if not restaurant_opration_detail:
                logger.error("Restaurant not found")
                return bad_request_response("Restaurant not found")

            # ✅ Return single restaurant as dict
            return handle_success_with_data(
                "Get Successfully restaurant operational.",
                restaurant_operational_to_dict(restaurant_opration_detail)
            )

        # If no operational_id, fetch all
        restaurant_opration_details = db.query(RestaurantOperationalDetails).all()
        logger.info("Restaurants fetched successfully: %s", restaurant_opration_details)

        # ✅ Return list of dicts
        return handle_success_with_data(
            "Get Successfully restaurant operational.",
            [restaurant_operational_to_dict(r) for r in restaurant_opration_details]
        )

    except Exception as e:
        logger.exception("Database error while fetching restaurant: %s", str(e))
        return server_error_response("Internal server error.")
