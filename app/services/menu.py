from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import Restaurant, Menu, RestruntShop
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


from app.services.s3_operations import delete_s3_folder_objects, upload_images_to_s3


async def add_menus(restaurant_data,menu_images,user_data, db):
    try:
        
        logger.info("restaurant_data: -----------------> %s",restaurant_data)
    
        # Check if Restaurant id with same name exists
        if not db.query(RestruntShop).filter(RestruntShop.shop_id == restaurant_data.shop_id).first():
            logger.error("Restaurant id not present: %s", restaurant_data.shop_id)
            return bad_request_response("Restaurant id not present.")
        
        if db.query(Menu).filter(Menu.shop_id == restaurant_data.shop_id, Menu.item_name == restaurant_data.item_name).first():
            logger.error("Item name all ready exits.")
            return bad_request_response("Item name all ready exits.")
        
        # Generate filenames
        # menu_images = generate_filename(menu_images)
        # logger.info("menu_images: -------------------> %s",menu_images)
        
        
        new_menu = Menu(
        shop_id=restaurant_data.shop_id,  # Replace with actual restaurant_id
        item_name=restaurant_data.item_name,
        description=restaurant_data.description,
        price=restaurant_data.price,
        discount_price=restaurant_data.discount_price,
        is_available=True,
        category_id=restaurant_data.category_id,  # Example JSON data
        veg_nonveg=restaurant_data.veg_nonveg,
        preparation_time=restaurant_data.preparation_time,
        # menu_images=menu_images # Example JSON list
        )

        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
        
        logger.info("Menu id: ------------------> %s",new_menu.menu_id)
        
        folder = f"menu/{new_menu.menu_id}"
        
        menu_images = await upload_images_to_s3([menu_images], folder)
        logger.info("menu_images: ------------------> %s",menu_images)
        
        menu = db.query(Menu).filter(Menu.menu_id == new_menu.menu_id).first()
        
        menu.menu_images = menu_images if menu_images else None
        
        # Commit changes
        db.commit()
        db.refresh(menu) 
        
   
        logger.info("Menu added successfully")
        return handle_success("Menu added restaurant.")
    except Exception as e:
        logger.exception("Database error while adding restaurant: %s", str(e))
        return server_error_response("Internal server error.")   




async def update_menus(restaurant_data,menu_images,user_data, db):
    try:
        
        logger.info("restaurant_data: -----------------> %s",restaurant_data)
        
        if not restaurant_data.menu_id :
            logger.error("Invalid menu id.")
            return bad_request_response("Invalid menu id.")
    

        # Check if Restaurant id with same name exists
        if not db.query(RestruntShop).filter(RestruntShop.shop_id == restaurant_data.shop_id).first():
            logger.error("Restaurant id not present: %s", restaurant_data.shop_id)
            return bad_request_response("Restaurant id not present.")
        
        # Menu Name check
        if db.query(Menu).filter(
            Menu.shop_id == restaurant_data.shop_id,
            Menu.item_name == restaurant_data.item_name,
            Menu.menu_id != restaurant_data.menu_id  # This is the NOT EQUAL condition
        ).first():
            logger.error("Item name already exists.")
            return bad_request_response("Item name already exists.")
        
        
        # Generate filenames
        menu_images = generate_filename(menu_images)
        logger.info("menu_images: -------------------> %s",menu_images)
        
        
        # Update menu data
        menu_record = db.query(Menu).filter(Menu.menu_id == restaurant_data.menu_id).first()

        if not menu_record:
            return bad_request_response("Menu not found.")

        # Fields to update
        update_fields = [
            "shop_id", "item_name", "description", "price", "discount_price",
            "is_available", "category_id", "veg_nonveg", "preparation_time", "menu_images"
        ]

        for field in update_fields:
            value = getattr(restaurant_data, field, getattr(menu_record, field))

            # Special handling for menu_images
            if field == "menu_images" and value:
                value = menu_images

            setattr(menu_record, field, value)
            
        db.commit()
        db.refresh(menu_record)
        
        
        
        logger.info("Menu updated successfully")
        return handle_success("Menu updated restaurant.")
    except Exception as e:
        logger.exception("Database error while adding restaurant: %s", str(e))
        return server_error_response("Internal server error.")   


from ..query import menu



from collections import defaultdict

# def format_restaurant_menu(rows):
#     grouped = {}

#     for row in rows:
#         shop_id = row["shop_id"]

#         if shop_id not in grouped:
#             # Initialize restaurant-level details
#             grouped[shop_id] = {
#                 "shop_id": row["shop_id"],
#                 "restaurant_name": row["restaurant_name"],
#                 "address": row["address"],
#                 "logo": row["logo"],
#                 "restaurant_image": row["restaurant_image"],
#                 "vat_tax": row["vat_tax"],
#                 "cuisine": row["cuisine"],   # already processed earlier
#                 "food_type": row["food_type"],
#                 "zone": row["zone"],
#                 "latitude": row["latitude"],
#                 "longitude": row["longitude"],
#                 "status": row["status"],
#                 "restaurant_phone": row["restaurant_phone"],
#                 "delivery_type": row["delivery_type"],
#                 "is_open": row["is_open"],
#                 "menus": []  # collect menus here
#             }

#         # Add menu-level details
#         menu_data = {
#             "menu_id": row["menu_id"],
#             "item_name": row["item_name"],
#             "description": row["description"],
#             "price": row["price"],
#             "discount_price": row["discount_price"],
#             "is_available": row["is_available"],
#             "veg_nonveg": row["veg_nonveg"],
#             "preparation_time": row["preparation_time"],
#             "menu_images": row["menu_images"],
#             "category_name": row["category_name"]
#         }
#         grouped[shop_id]["menus"].append(menu_data)

#     # Convert dict → list
#     return list(grouped.values())

import json

def format_restaurant_menu(rows):
    grouped = {}

    for row in rows:
        shop_id = row["restaurant_id"]

        if shop_id not in grouped:
            grouped[shop_id] = {
                "shop_id": row["restaurant_id"],
                "restaurant_name": row["restaurant_name"],
                "address": row["address"],
                "logo": json.loads(row["logo"]) if row["logo"] else None,
                "restaurant_image":json.loads(row["restaurant_image"]) if row["restaurant_image"] else None,
                "kitchen_image":json.loads(row["kitchen_image"]) if row["kitchen_image"] else None,
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "status": row["status"],
                "is_open": row["is_open"],
                "menus": []
            }

        grouped[shop_id]["menus"].append({
            "menu_id": row["menu_id"],
            "item_name": row["item_name"],
            "description": row["description"],
            "price": row["price"],
            "discount_price": row["discount_price"],
            "is_available": row["is_available"],
            "veg_nonveg": row["veg_nonveg"],
            "preparation_time": row["preparation_time"],
            "menu_images":json.loads(row["menu_images"]) if row["menu_images"] else None,
            "category_name": row["category_name"]
        })

    return list(grouped.values())

# get filter filed 
async def get_menus(restaurant_id,restaurant_name, item_name, category_id, veg_nonveg, user_data, db):
    try:
        logger.info(f"restaurant_id: {restaurant_id}, item_name: {item_name}, category_id: {category_id}, veg_nonveg: {veg_nonveg}")
        
        # call the get query 
        data = menu.get_restaurant_menu(db, restaurant_id, restaurant_name, item_name, category_id, veg_nonveg)
        logger.info("Data: %s",data)
        
        
        rows = [dict(row) for row in data]

        # (after cuisine processing)
        final_data = format_restaurant_menu(rows)
                
        
        
        logger.info("Menu get successfully")
        return handle_success_with_data("Menu get restaurant.",final_data)
    except Exception as e:
        logger.exception("Database error while adding restaurant: %s", str(e))
        return server_error_response("Internal server error.")   

