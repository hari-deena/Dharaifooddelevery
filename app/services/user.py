from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
# from app.query.notification import get_notifications_by_customer,get_notifications_by_turf, fcm_token_field_names
# from app.query.queries import get_filtered_fields, get_first_record, insert_record, update_records
# from app.utils.email_templates import generate_booking_confirmation, generate_booking_cancellation, generate_turf_inactive_cancellation, generate_booking_completed, generate_turf_booking_confirmation_nad_cancelation
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import User
from app.core.logger_config import configure_logger
from app.utils import config
import asyncio
from app.utils import config
from ..utils.common import create_jwt_token
from sqlalchemy import update
logger = configure_logger('justplay')



async def signup(data,db):
    try:
        logger.info("Signup Data: %s",data)
        
        # Step 1: Check if user already exists
        existing_user = db.query(User).filter(User.mobile_number == data.mobile_number).first()
        if existing_user:
            logger.error("User already present")
            return bad_request_response("User already present.")
        
        # Step 2: Create new user
        new_user = User(
            user_name=data.user_name,
            mobile_number=data.mobile_number,
            role_id=data.role_id,
            status="ACTIVE"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        if not new_user:
            logger.error("User data insert error.")
            return server_error_response("User data insert error.")
        
        logger.info("Successfully signup the user")
        return handle_success("Successfully signup the user")

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response(str(e)) 
    
    
async def login(data,db):
    try:
        logger.info("Signup Data: %s",data)
        
        # Step 1: Check if user already exists
        existing_user = db.query(User).filter(User.mobile_number == data.mobile_number).first()
        if not existing_user:
            logger.error("User is not present.")
            return bad_request_response("User is not present.")
        
        user_data = {
                "user_id": existing_user.user_id,
                "user_name": existing_user.user_name,
                "role_id": existing_user.role_id
            }
        
        
        logger.info("User data: %s",user_data)
        
        
        token = create_jwt_token(user_data)
        logger.info("Token ----------------> %s",token)
        
        data = {"token":token}
       
        logger.info("Successfully login the user")
        return handle_success_with_data("Successfully login the user",data)

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response(str(e)) 
    
    
async def update_user(request, user_data, db):
    try:
        logger.info("User update Data: %s",request)
        logger.info("User data: %s",user_data)
        
        # Update the user table
        result = db.execute(
            update(User)
            .where(User.user_id == user_data["user_id"])
            .values(
                user_name=request.user_name,
                updated_at=datetime.utcnow()
            )
        )
        logger.info("Rowcount: %s", result.rowcount)
        if result.rowcount == 0:
            logger.error("User data updated error.")
            return server_error_response("User data updated error.")
        
        db.commit()
        
        logger.info("Successfully update the user")
        return handle_success("Successfully update the user")

    except Exception as e:
        logger.exception("Error during booking registration: %s", str(e))
        return server_error_response(str(e)) 
   
   
# Convert User ORM object to dict ---
def user_to_dict(user: User) -> dict:
    return {
        "user_id": user.user_id,
        "user_name": user.user_name,
        "mobile_number": user.mobile_number,
        "email": user.email,
        "role_id": user.role_id,
        "status": user.status,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }
   
async def get_user(user_id, role_id, db):
    logger.info("Fetching users with user_id=%s, role_id=%s", user_id, role_id)

    try:
        query = db.query(User)

        # Apply filters if provided
        if user_id is not None:
            query = query.filter(User.user_id == user_id)
        if role_id is not None:
            query = query.filter(User.role_id == role_id)

        # Case 1: Only user_id provided → expect exactly one user
        if user_id is not None and role_id is None:
            logger.info("User id only present.")
            user = query.first()
            if not user:
                logger.info("Invalid user id given")
                return bad_request_response(f"Invalid user_id User not found")
            return handle_success_with_data("User retrieved successfully", [user_to_dict(user)])

        # Case 2: Only role_id provided → return list (possibly empty)
        elif role_id is not None and user_id is None:
            logger.info("Role id only present.")
            
            users = query.all()
            if not users:
                return handle_success_with_data("Data not found", [user_to_dict(u) for u in users])
            return handle_success_with_data("Users retrieved successfully", [user_to_dict(u) for u in users])

        # Case 3: Both provided → expect exactly one user matching both
        elif user_id is not None and role_id is not None:
            logger.info("User id and Role is both present.")
            
            user = query.first()
            if not user:
                return bad_request_response(f"No user found with user_id={user_id} and role_id={role_id}")
            return handle_success_with_data("User retrieved successfully", [user_to_dict(user)])

        # Case 4: Neither provided → return all users
        else:
            logger.info("Get all user data.")
            users = db.query(User).all()
            return handle_success_with_data("All users retrieved successfully", [user_to_dict(u) for u in users])

    except Exception as e:
        logger.exception("Error in get_user service: %s", str(e))
        return server_error_response("Internal server error.")
   