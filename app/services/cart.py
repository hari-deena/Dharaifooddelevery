from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
# from app.query.notification import get_notifications_by_customer,get_notifications_by_turf, fcm_token_field_names
# from app.query.queries import get_filtered_fields, get_first_record, insert_record, update_records
# from app.utils.email_templates import generate_booking_confirmation, generate_booking_cancellation, generate_turf_inactive_cancellation, generate_booking_completed, generate_turf_booking_confirmation_nad_cancelation
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import User, Cart, Menu
from app.core.logger_config import configure_logger
from app.utils import config
import asyncio
from app.utils import config
from ..utils.common import create_jwt_token
from sqlalchemy import update
logger = configure_logger('justplay')

from sqlalchemy import and_


async def add_cart(request,user_data,db):
    try:
        
        logger.info("request : -----------> %s",request)
        logger.info("user_data   : -----------> %s",user_data  )
        
        existing_cart = db.query(Cart).filter(
            and_(
                Cart.menu_id == request.menu_id,
                Cart.user_id == user_data["user_id"]
            )
        ).first()

        if existing_cart:
            logger.error("Cart already present")
            existing_cart.quantity += 1  
            db.commit()
            db.refresh(existing_cart)
            logger.info("Cart updated successfully.")
            return handle_success("Cart updated successfully.")
        
        
        new_cart = Cart(
        user_id=user_data["user_id"],
        menu_id=request.menu_id
        )
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        
        
        
        logger.info("Successfully add  the cart")
        return handle_success("Successfully add  the cart")

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response("Internal server error.") 
    
    
    
    

async def get_cart(user_data,db):
    try:
        
        logger.info("user_data   : -----------> %s",user_data )
        
        user_id = user_data["user_id"]
        
        logger.info("user_id   : -----------> %s",user_id )
        
        
        cart_entries = db.query(Cart).filter(Cart.user_id == user_id).all()

        if not cart_entries:
            logger.error("No data found.")
            return handle_success_with_data("No data found.",[])

        # Prepare cart response with menu details
        cart_response = []
        for entry in cart_entries:
            menu = db.query(Menu).filter(Menu.menu_id == entry.menu_id).first()
            if menu:
                cart_response.append({
                    "cart_id": entry.cart_id,
                    "menu_id": menu.menu_id,
                    "item_name": menu.item_name,
                    "description": menu.description,
                    "price": menu.price,
                    "discount_price": menu.discount_price,
                    "is_available": menu.is_available,
                    "category_id": menu.category_id,
                    "veg_nonveg": menu.veg_nonveg,
                    "preparation_time": menu.preparation_time,
                    "menu_images": menu.menu_images,
                    "quantity": entry.quantity  
                })

        
        
        logger.info("Successfully get  the cart")
        return handle_success_with_data("Successfully get  the cart",cart_response)

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response("Internal server error.") 
    
    
    
    
    
async def delete_cart(cart_id,user_data,db):
    try:
        
        logger.info("cart_id : -----------> %s",cart_id)
        logger.info("user_data   : -----------> %s",user_data  )
        
        existing_cart = db.query(Cart).filter(
            and_(
                Cart.cart_id == cart_id,
                Cart.user_id == user_data["user_id"]
            )
        ).first()
        logger.error("existing_cart: ---------> %s",existing_cart)

        if not existing_cart:
            logger.error("Cart not found.")
            return bad_request_response("Cart not found.")
        
        
        cart_entry = db.query(Cart).filter(Cart.cart_id == cart_id).first()
         # Delete the entry
        db.delete(cart_entry)
        db.commit()
       
        logger.info("Successfully delete  the cart")
        return handle_success("Successfully delete  the cart")

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response("Internal server error.") 
  