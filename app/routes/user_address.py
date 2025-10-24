from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database_config import get_db
from app.services import user_address
from typing import Optional
from ..utils.response_handling import bad_request_response, handle_unauthorized_error
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from ..schemas.user_address import UserAddress
from app.core.logger_config import configure_logger
from ..routes.user import verify_token
logger = configure_logger('dharaifood')

from ..utils.response_handling import CustomAuthException

user_address_router = APIRouter()


@user_address_router.post("/add_address")
async def add_address(
    request: UserAddress,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await user_address.add_address(request,user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)



@user_address_router.put("/address_select/{address_id}")
async def address_select(
    address_id : int,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await user_address.address_select(address_id,user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)




@user_address_router.put("/update_address/{address_id}")
async def update_address(
    address_id : int,
    request: UserAddress,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await user_address.update_address(address_id, request, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)



@user_address_router.get("/get_address")
async def get_address(
    address_id : Optional[int] = Query(None, description="Address id using get address data."),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await user_address.get_address(address_id, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)

