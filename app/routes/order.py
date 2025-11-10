from fastapi import APIRouter, UploadFile, Depends,Form, File, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database_config import get_db
from app.services import order
from typing import Optional, List
from ..utils.response_handling import bad_request_response, handle_unauthorized_error
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from ..schemas.order import OrderPayload, RestaurantOrderStatusRequest
from app.core.logger_config import configure_logger
logger = configure_logger('justplay')
from ..utils.response_handling import CustomAuthException
from .user import verify_token


order_router = APIRouter()




@order_router.post("/place")
async def add_order(
    request: OrderPayload,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await order.add_order(request, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)

    
    
@order_router.get("/get_user_order")
async def get_user_order(
    user_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    order_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    status : Optional[str] = Query(None, description="restaurant id using get feedback"),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await order.get_user_order(user_id, order_id, status, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)



@order_router.get("/get_restrunt_orders")
async def get_shop_order(
    shop_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    rest_status : Optional[str] = Query(None, description="restaurant verification_status  using get feedback"),
    db: Session = Depends(get_db),
    # user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await order.get_shop_orders(shop_id, rest_status, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)




@order_router.post("/restrunt_accept")
async def restrunt_accept(
    request: RestaurantOrderStatusRequest,
    db: Session = Depends(get_db),
    # user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await order.restrunt_accept(request, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)
  
