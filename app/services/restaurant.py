from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
# from app.query.notification import get_notifications_by_customer,get_notifications_by_turf, fcm_token_field_names
# from app.query.queries import get_filtered_fields, get_first_record, insert_record, update_records
# from app.utils.email_templates import generate_booking_confirmation, generate_booking_cancellation, generate_turf_inactive_cancellation, generate_booking_completed, generate_turf_booking_confirmation_nad_cancelation
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import Restaurant
from app.core.logger_config import configure_logger
from app.utils import config
import asyncio
from app.utils import config
from ..utils.common import create_jwt_token
from sqlalchemy import update
from uuid import uuid4
logger = configure_logger('justplay')


def generate_filename(file):
    """Generate a unique filename for uploaded files."""
    return f"{uuid4()}_{file.filename}"



# async def add_restrunt(restaurant_data,logo,restaurant_image, user_data, db):
#     try:
#         logger.info("Resterunt Data: %s",restaurant_data)
#         logger.info("Logo:  %s",logo)
#         logger.info("restaurant_image:  %s",restaurant_image)
#         logger.info("user_data: --------> %s", user_data)
        
#         existing_restaurant = db.query(Restaurant).filter(
#         Restaurant.restaurant_name == restaurant_data.restaurant_name
#         ).first()

#         if existing_restaurant:
#             logger.error("Restaurant with this name already exists")
#             return bad_request_response("Restaurant with this name already exists")
        
#         check_restaurant = db.query(Restaurant).filter(
#         Restaurant.owner_id == user_data["user_id"]
#         ).first()

#         if check_restaurant:
#             logger.error("You have already register your restaurant.")
#             return bad_request_response("You have already register your restaurant.")
        
        
#         logo_filename = f"{uuid4()}_{logo.filename}"
#         image_filename = f"{uuid4()}_{restaurant_image.filename}"
        
        
#         # 🔹 Step 3: Insert into DB
#         new_restaurant = Restaurant(
#             owner_id=user_data["user_id"],
#             restaurant_name=restaurant_data.restaurant_name,
#             address=restaurant_data.address,
#             vat_tax=restaurant_data.vat_tax,
#             cuisine=restaurant_data.cuisine,  # should already be list/dict for JSON
#             food_type=restaurant_data.food_type,
#             zone=restaurant_data.zone,
#             latitude=restaurant_data.latitude,
#             longitude=restaurant_data.longitude,
#             restaurant_phone=restaurant_data.restaurant_phone,
#             delivery_type=restaurant_data.delivery_type,
#             logo=logo_filename,
#             restaurant_image=image_filename,
#         )

#         db.add(new_restaurant)
#         db.commit()
#         db.refresh(new_restaurant)
        
       
#         logger.info("Successfully restrunt added.")
#         return handle_success("Successfully restrunt added.")

#     except Exception as e:
#         logger.exception("Error during booking registration: %s", str(e))
#         return server_error_response("Internal server error.") 
    
 
async def add_restaurant(restaurant_data, logo, restaurant_image, user_data, db):
    logger.info("Adding restaurant for user_id: %s", user_data["user_id"])

    # Check if restaurant with same name exists
    if db.query(Restaurant).filter(Restaurant.restaurant_name == restaurant_data.restaurant_name).first():
        logger.error("Restaurant with this name already exists: %s", restaurant_data.restaurant_name)
        return bad_request_response("Restaurant with this name already exists")

    # Check if user already has a restaurant
    if db.query(Restaurant).filter(Restaurant.owner_id == user_data["user_id"]).first():
        logger.error("User already registered a restaurant: %s", user_data["user_id"])
        return bad_request_response("You have already registered your restaurant.")

    # Generate filenames
    logo_filename = generate_filename(logo)
    image_filename = generate_filename(restaurant_image)

    # Create restaurant object
    new_restaurant = Restaurant(
        owner_id=user_data["user_id"],
        logo=logo_filename,
        restaurant_image=image_filename
    )

    # Assign fields dynamically
    for field in [
        "restaurant_name", "address", "vat_tax", "cuisine",
        "food_type", "zone", "latitude", "longitude",
        "restaurant_phone", "delivery_type"
    ]:
        setattr(new_restaurant, field, getattr(restaurant_data, field))

    try:
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)
        logger.info("Restaurant added successfully: %s", new_restaurant.restaurant_id)
        return handle_success("Successfully added restaurant.")
    except Exception as e:
        logger.exception("Database error while adding restaurant: %s", str(e))
        return server_error_response("Internal server error.")   


# async def update_restrunt(restaurant_data,logo,restaurant_image, user_data, db):
#     try:
#         logger.info("Resterunt Data: %s",restaurant_data)
#         logger.info("Logo:  %s",logo)
#         logger.info("restaurant_image:  %s",restaurant_image)
#         logger.info("user_data: --------> %s", user_data)
        
#         logo_filename = f"{uuid4()}_{logo.filename}"
#         image_filename = f"{uuid4()}_{restaurant_image.filename}"
        
        
#         existing_restaurant = db.query(Restaurant).filter(
#         Restaurant.restaurant_id == restaurant_data.restaurant_id
#         ).first()
        
#         if not existing_restaurant:
#             logger.error("Invalid restaurant id.")
#             return bad_request_response("Invalid restaurant id.")
        
    
#         existing_restaurant_name = db.query(Restaurant).filter(
#             Restaurant.restaurant_name == restaurant_data.restaurant_name,
#             Restaurant.restaurant_id != restaurant_data.restaurant_id  # Exclude current restaurant
#         ).first()
        
#         if existing_restaurant_name:
#             logger.error("Restaurant with this name already exists")
#             return bad_request_response("Restaurant with this name already exists")
        
        
#         # Update the fields
#         existing_restaurant.restaurant_name = restaurant_data.restaurant_name
#         existing_restaurant.address = restaurant_data.address
#         existing_restaurant.vat_tax = restaurant_data.vat_tax
#         existing_restaurant.cuisine = restaurant_data.cuisine  # list/dict for JSON
#         existing_restaurant.food_type = restaurant_data.food_type
#         existing_restaurant.zone = restaurant_data.zone
#         existing_restaurant.latitude = restaurant_data.latitude
#         existing_restaurant.longitude = restaurant_data.longitude
#         existing_restaurant.restaurant_phone = restaurant_data.restaurant_phone
#         existing_restaurant.delivery_type = restaurant_data.delivery_type
#         existing_restaurant.logo = logo_filename
#         existing_restaurant.restaurant_image = image_filename

#         # Commit the changes
#         db.commit()
#         db.refresh(existing_restaurant)
       
#         logger.info("Successfully restrunt Updated.")
#         return handle_success("Successfully restrunt Updated.")

#     except Exception as e:
#         logger.exception("Error during booking registration: %s", str(e))
#         return server_error_response("Internal server error.") 
   
   
   
   

async def update_restaurant(restaurant_data, logo, restaurant_image, user_data, db):
    logger.info("Updating restaurant: %s", restaurant_data.restaurant_id)

    # Generate filenames
    logo_filename = generate_filename(logo)
    image_filename = generate_filename(restaurant_image)

    # Fetch the existing restaurant
    existing_restaurant = db.query(Restaurant).filter(
        Restaurant.restaurant_id == restaurant_data.restaurant_id
    ).first()

    if not existing_restaurant:
        logger.error("Restaurant ID not found.")
        return bad_request_response("Invalid restaurant id.")

    # Check for duplicate restaurant name
    duplicate_name = db.query(Restaurant).filter(
        Restaurant.restaurant_name == restaurant_data.restaurant_name,
        Restaurant.restaurant_id != restaurant_data.restaurant_id
    ).first()
    if duplicate_name:
        logger.error("Duplicate restaurant name: %s", restaurant_data.restaurant_name)
        return bad_request_response("Restaurant with this name already exists")

    # Update fields
    for field in [
        "restaurant_name", "address", "vat_tax", "cuisine",
        "food_type", "zone", "latitude", "longitude",
        "restaurant_phone", "delivery_type"
    ]:
        setattr(existing_restaurant, field, getattr(restaurant_data, field))

    existing_restaurant.logo = logo_filename
    existing_restaurant.restaurant_image = image_filename

    try:
        db.commit()
        db.refresh(existing_restaurant)
        logger.info("Restaurant updated successfully: %s", existing_restaurant.restaurant_id)
        return handle_success("Successfully updated restaurant.")
    except Exception as e:
        logger.exception("Database error while updating restaurant: %s", str(e))
        return server_error_response("Internal server error.")   


def restaurant_to_dict(restaurant: Restaurant):
    return {
        "restaurant_id": restaurant.restaurant_id,
        "owner_id": restaurant.owner_id,
        "restaurant_name": restaurant.restaurant_name,
        "address": restaurant.address,
        "logo": restaurant.logo,
        "restaurant_image": restaurant.restaurant_image,
        "vat_tax": restaurant.vat_tax,
        "cuisine": restaurant.cuisine,
        "food_type": restaurant.food_type.value if restaurant.food_type else None,
        "zone": restaurant.zone,
        "latitude": restaurant.latitude,
        "longitude": restaurant.longitude,
        "status": restaurant.status,
        "restaurant_phone": restaurant.restaurant_phone,
        "delivery_type": restaurant.delivery_type.value if restaurant.delivery_type else None,
        "created_at": restaurant.created_at.isoformat() if restaurant.created_at else None,   # 👈 FIX
        "updated_at": restaurant.updated_at.isoformat() if restaurant.updated_at else None,   # 👈 FIX
    }


# Get Restrunt API
# async def get_restaurant(restaurant_id, user_data, db):
    
#     try:
        
#         logger.info("Restaurant id: ----------> %s",restaurant_id)
#         logger.info("User data: ---------------> %s",user_data)
        
#         if restaurant_id:
#             # Fetch single restaurant
#             restaurant = db.query(Restaurant).filter(
#                 Restaurant.restaurant_id == restaurant_id,
#                 Restaurant.status == "ACTIVE"
#             ).first()

#             if not restaurant:
#                 logger.error("Restaurant not found")
#                 return bad_request_response("Restaurant not found")

#             # return restaurant
#             return handle_success_with_data("Successfully get the Restaurant",restaurant)

#         # Fetch all active restaurants
#         restaurants = db.query(Restaurant).filter(Restaurant.status == "ACTIVE").all()
#         # return restaurants
        
#         logger.info("Restaurant get successfully")
#         return handle_success_with_data("Successfully get restaurant.",[restaurant_to_dict(r) for r in restaurants])
#     except Exception as e:
#         logger.exception("Database error while updating restaurant: %s", str(e))
#         return server_error_response("Internal server error.")   


async def get_restaurant(restaurant_id, user_data, db):
    try:
        logger.info("Restaurant id: %s", restaurant_id)
        logger.info("User data: %s", user_data)

        if restaurant_id:
            restaurant = db.query(Restaurant).filter(
                Restaurant.restaurant_id == restaurant_id,
                Restaurant.status == "ACTIVE"
            ).first()

            if not restaurant:
                logger.error("Restaurant not found")
                return bad_request_response("Restaurant not found")

            return handle_success_with_data(
                "Successfully fetched restaurant.",
                restaurant_to_dict(restaurant)
            )

        restaurants = db.query(Restaurant).filter(Restaurant.status == "ACTIVE").all()
        logger.info("Restaurants fetched successfully")
            
        return handle_success_with_data(
            "Successfully fetched restaurants.",
            [restaurant_to_dict(r) for r in restaurants]
        )

    except Exception as e:
        logger.exception("Database error while fetching restaurant: %s", str(e))
        return server_error_response("Internal server error.")
