from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
# from app.query.notification import get_notifications_by_customer,get_notifications_by_turf, fcm_token_field_names
# from app.query.queries import get_filtered_fields, get_first_record, insert_record, update_records
# from app.utils.email_templates import generate_booking_confirmation, generate_booking_cancellation, generate_turf_inactive_cancellation, generate_booking_completed, generate_turf_booking_confirmation_nad_cancelation
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import Restaurant, RestruntShop
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
        logger.info("Restaurant added successfully: %s", new_restaurant.shop_id)
        return handle_success("Successfully added restaurant.")
    except Exception as e:
        logger.exception("Database error while adding restaurant: %s", str(e))
        return server_error_response("Internal server error.")   

   

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











# --------------------------------------- new code ------------------------------------------
from sqlalchemy import and_

# async def add_shop(shop_data , user_data, db):

#     try:
#         logger.info("Shop details : %s", shop_data)
#         logger.info("User data: %s",user_data)
        
#         # Check if restaurant with same name exists
#         if db.query(RestruntShop).filter(
#     and_(
#                 RestruntShop.shop_name == shop_data.shop_name,
#                 RestruntShop.shop_address == shop_data.shop_address
#             )
#         ).first():
#             logger.error("Restaurant with this name already exists: %s", shop_data.shop_name)
#             return bad_request_response("Restaurant with this name already exists")
        
        
#          # Create RestruntShop object
#         new_shop = RestruntShop(
#             owner_id=user_data["user_id"],
#             shop_name=shop_data.shop_name,
#             shop_address=shop_data.shop_address,
#             GST_license=shop_data.GST_license,
#             fssai=shop_data.fssai,
#             pan=shop_data.pan,
#             bank_name=shop_data.bank_name,
#             account_number=shop_data.account_number,
#             ifsc_code=shop_data.ifsc_code,
#             is_open=False,  # default
#             verification_status='PENDING',
#             status='ACTIVE'
#         )

#         # Add to database
#         db.add(new_shop)
#         db.commit()
#         db.refresh(new_shop)  # refresh to get auto-generated shop_id
            
       
#         return handle_success("Successfully added shop details.")
#     except Exception as e:
#         logger.exception("Database error while updating restaurant: %s", str(e))
#         return server_error_response("Internal server error.")   


from sqlalchemy import and_
from fastapi import HTTPException

async def add_shop(shop_data, user_data, db):
    try:
        logger.info("Shop details : %s", shop_data)
        logger.info("User data: %s", user_data)

        # ✅ Case 1: Update existing shop if shop_id is provided
        if getattr(shop_data, "shop_id", None):
            existing_shop = db.query(RestruntShop).filter(
                RestruntShop.shop_id == shop_data.shop_id,
                RestruntShop.owner_id == user_data["user_id"],
                RestruntShop.status == "ACTIVE"
            ).first()

            if not existing_shop:
                logger.error("Shop ID %s not found for update", shop_data.shop_id)
                return bad_request_response("Shop not found for update")

            # ✅ Check if another shop has the same name (excluding this shop)
            duplicate_shop = db.query(RestruntShop).filter(
                and_(
                    RestruntShop.shop_name == shop_data.shop_name,
                    RestruntShop.shop_id != shop_data.shop_id,
                    RestruntShop.status == "ACTIVE"
                )
            ).first()

            if duplicate_shop:
                logger.error("Another shop already exists with name: %s", shop_data.shop_name)
                return bad_request_response("Another shop already exists with this name")

            # ✅ Update fields
            existing_shop.shop_name = shop_data.shop_name or existing_shop.shop_name
            existing_shop.shop_address = shop_data.shop_address or existing_shop.shop_address
            existing_shop.GST_license = shop_data.GST_license or existing_shop.GST_license
            existing_shop.fssai = shop_data.fssai or existing_shop.fssai
            existing_shop.pan = shop_data.pan or existing_shop.pan
            existing_shop.bank_name = shop_data.bank_name or existing_shop.bank_name
            existing_shop.account_number = shop_data.account_number or existing_shop.account_number
            existing_shop.ifsc_code = shop_data.ifsc_code or existing_shop.ifsc_code

            db.commit()
            db.refresh(existing_shop)

            logger.info("Shop updated successfully: %s", existing_shop.shop_id)
            return handle_success(f"Shop details updated successfully.")

        # ✅ Case 2: Insert new shop if no shop_id provided
        else:
            # Check if restaurant with same name & address exists
            if db.query(RestruntShop).filter(
                and_(
                    RestruntShop.shop_name == shop_data.shop_name,
                    RestruntShop.shop_address == shop_data.shop_address
                )
            ).first():
                logger.error("Restaurant with this name already exists: %s", shop_data.shop_name)
                return bad_request_response("Restaurant with this name already exists")

            new_shop = RestruntShop(
                owner_id=user_data["user_id"],
                shop_name=shop_data.shop_name,
                shop_address=shop_data.shop_address,
                GST_license=shop_data.GST_license,
                fssai=shop_data.fssai,
                pan=shop_data.pan,
                bank_name=shop_data.bank_name,
                account_number=shop_data.account_number,
                ifsc_code=shop_data.ifsc_code,
                is_open=False,
                verification_status='PENDING',
                status='ACTIVE'
            )

            db.add(new_shop)
            db.commit()
            db.refresh(new_shop)

            logger.info("New shop added successfully: %s", new_shop.shop_id)
            return handle_success(f"Shop added successfully.")

    except Exception as e:
        logger.exception("Database error while adding/updating restaurant: %s", str(e))
        return server_error_response("Internal server error.")




def shop_to_dict(shop: RestruntShop):
    return {
        "shop_id": shop.shop_id or "",
        "owner_id": shop.owner_id or "",
        "shop_name": shop.shop_name or "",
        "shop_address": shop.shop_address or "",
        "latitude": shop.latitude if shop.latitude is not None else "",
        "logtitude": shop.logtitude if shop.logtitude is not None else "",
        "GST_license": shop.GST_license or "",
        "fssai": shop.fssai or "",
        "pan": shop.pan or "",
        "bank_name": shop.bank_name or "",
        "account_number": shop.account_number or "",
        "ifsc_code": shop.ifsc_code or "",
        "logo": shop.logo or {},
        "banner": shop.banner or {},
        "kitchen_image": shop.kitchen_image or {},
        "is_open": shop.is_open if shop.is_open is not None else False,
        "verification_status": shop.verification_status or "PENDING",
        "reson_for_rejection": shop.reson_for_rejection or "",
        "status": shop.status or "ACTIVE",
        "created_at": shop.created_at.isoformat() if shop.created_at else "",
        "updated_at": shop.updated_at.isoformat() if shop.updated_at else ""
    }




# async def get_shop(shop_id, verification_status, user_data, db):
#     try:
#         logger.info("Restaurant id: %s", shop_id)
#         logger.info("User data: %s", user_data)

#         if shop_id:
#             restaurant = db.query(RestruntShop).filter(
#                 RestruntShop.shop_id == shop_id,
#                 RestruntShop.status == "ACTIVE"
#             ).first()

#             if not restaurant:
#                 logger.error("Restaurant not found")
#                 return bad_request_response("Restaurant not found")

#             return handle_success_with_data(
#                 "Successfully fetched restaurant.",
#                 shop_to_dict(restaurant)
#             )

#         restaurants = db.query(RestruntShop).filter(RestruntShop.status == "ACTIVE").all()
#         logger.info("Restaurants fetched successfully")
            
#         return handle_success_with_data(
#             "Successfully fetched restaurants.",
#             [shop_to_dict(r) for r in restaurants]
#         )

#     except Exception as e:
#         logger.exception("Database error while fetching restaurant: %s", str(e))
#         return server_error_response("Internal server error.")


async def get_shop(shop_id, verification_status, user_data, db):
    try:
        logger.info("Restaurant id: %s", shop_id)
        logger.info("User data: %s", user_data)

        query = db.query(RestruntShop).filter(RestruntShop.status == "ACTIVE")

        # Filter by shop_id if provided
        if shop_id:
            query = query.filter(RestruntShop.shop_id == shop_id)

        # Filter by verification_status if provided
        if verification_status:
            allowed_status = ["PENDING","APPROVED", "REJECTED"]
            if verification_status not in allowed_status:
                return bad_request_response(f"Invalid verification_status. Allowed values: {allowed_status}")
            query = query.filter(RestruntShop.verification_status == verification_status)

        restaurants = query.all()

        if not restaurants:
            return handle_success("No restaurants found.")

        # If single shop_id requested, return first restaurant
        if shop_id:
            return handle_success_with_data(
                "Successfully fetched restaurant.",
                shop_to_dict(restaurants[0])
            )

        return handle_success_with_data(
            "Successfully fetched restaurants.",
            [shop_to_dict(r) for r in restaurants]
        )

    except Exception as e:
        logger.exception("Database error while fetching restaurant: %s", str(e))
        return server_error_response("Internal server error.")


async def shop_verification(shop_data , db):

    try:
        logger.info("Shop details : %s", shop_data)
        
        # Fetch the shop object
        shop = db.query(RestruntShop).filter(RestruntShop.shop_id == shop_data.shop_id).first()
        if not shop:
            logger.info(f"Shop with id {shop_data.shop_id} not found")
            return bad_request_response(f"Shop with id {shop_data.shop_id} not found")
        
        # Update fields
        shop.verification_status = shop_data.verification_status
        shop.reson_for_rejection = shop_data.reason if shop_data.reason else None
        
        # Commit changes
        db.commit()
        db.refresh(shop) 
        
         # Create RestruntShop object
          
        logger.info("Successfully verification.")
        return handle_success("Successfullyverification.")
    except Exception as e:
        logger.exception("Database error while updating restaurant: %s", str(e))
        return server_error_response("Internal server error.")   



# Images add Api 

from app.services.s3_operations import upload_images_to_s3, delete_s3_folder_objects

async def add_shop_imaes(shop_id,logo,shop_image,banner, db):

    try:
        logger.info("shop_id  : %s", shop_id)
        logger.info("logo  : %s", logo)
        logger.info("shop_image  : %s", shop_image)
        logger.info("banner  : %s", banner)
        
        # Fetch the shop object
        shop = db.query(RestruntShop).filter(RestruntShop.shop_id == shop_id).first()
        if not shop:
            logger.info(f"Shop with id {shop_id} not found")
            return bad_request_response(f"Shop with id {shop_id} not found")
        
        
        folder = f"shop/{shop_id}"
        
        delete_image = delete_s3_folder_objects(folder)
        logger.info("delete_image: --------------> %s",delete_image)
        
        logo_urls = await upload_images_to_s3([logo], folder)
        logger.info("logo_urls: ------------------> %s",logo_urls)
        
        shop_image_urls = await upload_images_to_s3([shop_image], folder)
        logger.info("shop_image_urls: ------------------> %s",shop_image_urls)
        
        banner_urls = await upload_images_to_s3([banner], folder)
        logger.info("banner_urls: ------------------> %s",banner_urls)
        
        
        shop.logo = logo_urls if logo_urls else None
        shop.banner = banner_urls if banner_urls else None
        shop.kitchen_image = shop_image_urls if shop_image_urls else None
        
        
        # Commit changes
        db.commit()
        db.refresh(shop) 
          
        logger.info("Successfully updated images.")
        return handle_success("Successfully updated images.")
    except Exception as e:
        logger.exception("Database error while updating restaurant: %s", str(e))
        return server_error_response("Internal server error.")   
