from fastapi import APIRouter, UploadFile, Depends,Form, File, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database_config import get_db
from app.services import restaurant_operational
from typing import Optional, List
from ..utils.response_handling import bad_request_response, handle_unauthorized_error
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from ..schemas.restaurant_operational import RestaurantOperationalDetailsSchema , RestaurantIsOpenDetailsSchema
from app.core.logger_config import configure_logger
logger = configure_logger('justplay')
from ..utils.response_handling import CustomAuthException
from .user import verify_token


restaurant_operational_router = APIRouter()



@restaurant_operational_router.post("/add_or_update_restaurant_operational")
async def add_restaurant_operational(
    request: RestaurantOperationalDetailsSchema,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        
        
        return await restaurant_operational.add_operational_restaurant(request, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)



@restaurant_operational_router.put("/update_is_open/{operational_id}")
async def update_is_open(
    operational_id : int,
    request: RestaurantIsOpenDetailsSchema,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await restaurant_operational.update_is_open(operational_id, request, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)


@restaurant_operational_router.put("/get_operational")
async def update_is_open(
    operational_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        print("------------------>")
        return await restaurant_operational.update_is_open(operational_id, request, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)



@restaurant_operational_router.get("/get_restaurant_operational")
async def get_restaurant_operational(
    operational_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await restaurant_operational.get_restaurant_operational(operational_id,user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)
