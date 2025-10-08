from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database_config import get_db
from app.services import user
from typing import Optional
from ..utils.response_handling import bad_request_response, handle_unauthorized_error
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from ..schemas.user import UserSchema, LoginUserSchema, UpdateUserSchema
from app.core.logger_config import configure_logger
logger = configure_logger('justplay')

from ..utils.response_handling import CustomAuthException

user_router = APIRouter()

from ..utils.common import decode_jwt_token
# dependencies.py (or wherever you prefer)
from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from app.models.table_management import User


async def verify_token(token: Optional[str] = Header(None), db: Session = Depends(get_db) ):
    # db = get_db()
    if not token:
        logger.error("Authorization header missing")
        raise CustomAuthException("Authorization header missing")
    logger.info("token --------------------> %s",token)
    
    status, data = decode_jwt_token(token)  # <-- your JWT decoder
    logger.info("User data: -----> %s",data)
    if not status:
        raise CustomAuthException(data)
    
    existing_user = db.query(User).filter(User.user_id == data["user_id"]).first()
    logger.info("existing_user ----------> userId: %s",existing_user)
    if not existing_user:
        logger.error("User already present")
        return bad_request_response("User already present.")

    return data




@user_router.post("/signup")
async def signup(
    request: UserSchema,
    db: Session = Depends(get_db)
):
    try:
        return await user.signup(request, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)




@user_router.post("/login")
async def login(
    request: LoginUserSchema,
    db: Session = Depends(get_db)
):
    try:
        return await user.login(request, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)


@user_router.put("/update_user")
async def update_user(
    request: UpdateUserSchema,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
):
    try:
        return await user.update_user(request,user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)


@user_router.get("/get_user")
async def get_user(
    user_id : Optional[int] = Query(None, description="User id using get feedback"),
    role_id : Optional[int] = Query(None, description="User id using get feedback"),
    db: Session = Depends(get_db),
):
    try:
        return await user.get_user(user_id,role_id, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)
