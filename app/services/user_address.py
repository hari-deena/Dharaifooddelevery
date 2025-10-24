from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
# from app.query.notification import get_notifications_by_customer,get_notifications_by_turf, fcm_token_field_names
# from app.query.queries import get_filtered_fields, get_first_record, insert_record, update_records
# from app.utils.email_templates import generate_booking_confirmation, generate_booking_cancellation, generate_turf_inactive_cancellation, generate_booking_completed, generate_turf_booking_confirmation_nad_cancelation
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import User, UserAddress
from app.core.logger_config import configure_logger
from app.utils import config
import asyncio
from app.utils import config
from ..utils.common import create_jwt_token
from sqlalchemy import update
from app.services.s3_operations import upload_images_to_s3, delete_s3_folder_objects

logger = configure_logger('justplay')

from sqlalchemy import func



async def add_address(data,user_data,db):
    try:
        logger.info("Address Data: %s",data)
        logger.info("user_data: -------> %s",user_data)
        
        # normalize incoming values for comparison (strip whitespace)
        addr_details_in = (data.address_details or "").strip()
        delivery_details_in = (data.delivery_details or "").strip()
        
        
        # 1) Check duplicate where BOTH fields match (case-insensitive)
        duplicate = (
            db.query(UserAddress)
            .filter(UserAddress.user_id == user_data["user_id"])
            .filter(
                func.lower(func.coalesce(UserAddress.address_details, "")) == addr_details_in.lower(),
                func.lower(func.coalesce(UserAddress.delivery_details, "")) == delivery_details_in.lower()
            )
            .first()
        )

        if duplicate:
            logger.error("Address already exists for this user.")
            return bad_request_response("Address already exists for this user.")
        
        existing_user = db.query(UserAddress).filter(UserAddress.user_id == user_data["user_id"]).first()
        is_active = True
        
        if existing_user:
            is_active = False
            
            
        new_address = UserAddress(
        user_id=user_data["user_id"],
        delivery_details=data.delivery_details,
        address_details=data.address_details,
        receiver_name=data.receiver_name,
        receiver_phone=data.receiver_phone,
        address_save_as=data.address_save_as,
        is_active=is_active
    )
        
        db.add(new_address)
        db.commit()
        db.refresh(new_address) 
            
        logger.info(f"Is active: ------------> {is_active}")
        
        
        logger.info("Successfully added the user address.")
        return handle_success("Successfully added the user address.")

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response(str(e)) 
 
 
 
async def address_select(address_id,user_data,db):
    try:
        logger.info("address_id: %s",address_id)
        logger.info("user_data: -------> %s",user_data)
        
        if not address_id:
            logger.error("Invalid address id.")
            return bad_request_response("Invalid address id.")
        
        db.query(UserAddress).filter(UserAddress.user_id == user_data["user_id"]).update(
            {UserAddress.is_active: False}, synchronize_session=False
        )

        # Step 2: Activate the selected address
        result = db.query(UserAddress).filter(
            UserAddress.user_id == user_data["user_id"],
            UserAddress.address_id == address_id
        ).update({UserAddress.is_active: True}, synchronize_session=False)

        # Step 3: Commit the changes
        db.commit()
        
        if result == 0:
            logger.error("Address not found for the given user_id.")
            return bad_request_response("Address not found for the given user_id.")
        
        logger.info("Active address updated successfully")
        return handle_success("Active address updated successfully")

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response(str(e)) 
 
 
 
async def update_address(address_id, data, user_data, db):
    try:
        logger.info("address_id: %s",address_id)
        logger.info("user_data: -------> %s",user_data)
        logger.info("data: -----------------> %s",data)
        
        if not address_id:
            logger.error("Invalid address id.")
            return bad_request_response("Invalid address id.")
        
        
        addr_details_in = (data.address_details or "").strip()
        delivery_details_in = (data.delivery_details or "").strip()

        # ✅ Check duplicate where BOTH fields match (case-insensitive)
        duplicate = (
            db.query(UserAddress)
            .filter(UserAddress.user_id == user_data["user_id"])
            .filter(UserAddress.address_id != address_id)  # 👈 exclude current record
            .filter(
                func.lower(func.coalesce(UserAddress.address_details, "")) == addr_details_in.lower(),
                func.lower(func.coalesce(UserAddress.delivery_details, "")) == delivery_details_in.lower()
            )
            .first()
        )

        if duplicate:
            logger.error("Address already exists for this user.")
            return bad_request_response("Address already exists for this user.")
        
        # Find the address that belongs to this user and has the given address_id
        existing_address = (
            db.query(UserAddress)
            .filter(
                UserAddress.user_id == user_data["user_id"],
                UserAddress.address_id == address_id
            )
            .first()
        )

        if not existing_address:
            logger.error("Address not found for this user.")
            return bad_request_response("Address not found for this user.")

        # ✅ Update fields
        existing_address.delivery_details = data.delivery_details
        existing_address.address_details = data.address_details
        existing_address.receiver_name = data.receiver_name
        existing_address.receiver_phone = data.receiver_phone
        existing_address.address_save_as = data.address_save_as

        # Commit the changes
        db.commit()
        db.refresh(existing_address)

                
       
        logger.info("Address updated successfully")
        return handle_success("Address updated successfully")

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response(str(e)) 
 
 


async def get_address(address_id,user_data,db):
    try:
        logger.info("address_id: %s",address_id)
        logger.info("user_data: -------> %s",user_data)
        
        
        if address_id:
            # 1️⃣ Fetch specific address
            address = db.query(UserAddress).filter(
                UserAddress.user_id == user_data["user_id"],
                UserAddress.address_id == address_id
            ).first()

            if not address:
                logger.error("Invalid address id")
                return bad_request_response("Invalid address id")

            # Return single address as dict
            data = {
                "address_id": address.address_id,
                "user_id": address.user_id,
                "delivery_details": address.delivery_details,
                "address_details": address.address_details,
                "receiver_name": address.receiver_name,
                "receiver_phone": address.receiver_phone,
                "address_save_as": address.address_save_as,
                "is_active": address.is_active
            }
            
            logger.info("Get Address successfully")
            return handle_success_with_data("Get Address successfully",data)


        else:
            # 2️⃣ Fetch all addresses for the user
            addresses = db.query(UserAddress).filter(UserAddress.user_id == user_data["user_id"]).all()

            if not addresses:
                logger.info("No addresses found.")
                return handle_success_with_data("No addresses found",[])

            # Return list of addresses as dicts
            data =  [
                {
                    "address_id": addr.address_id,
                    "user_id": addr.user_id,
                    "delivery_details": addr.delivery_details,
                    "address_details": addr.address_details,
                    "receiver_name": addr.receiver_name,
                    "receiver_phone": addr.receiver_phone,
                    "address_save_as": addr.address_save_as,
                    "is_active": addr.is_active
                }
                for addr in addresses
            ]
            
            logger.info("Get Address successfully")
            return handle_success_with_data("Get Address successfully",data)

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response(str(e)) 
 