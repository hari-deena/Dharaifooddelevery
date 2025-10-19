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
from ..services import cart
from ..schemas.cart import CartRequest
from .user import verify_token


cart_router = APIRouter()


@cart_router.post("/add_cart")
async def add_cart(
    request: CartRequest,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await cart.add_cart(request,user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)



@cart_router.get("/get_cart")
async def get_cart(
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await cart.get_cart(user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)



@cart_router.delete("/delete_cart/{cart_id}")
async def delete_cart(
    cart_id : int ,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await cart.delete_cart(cart_id, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)
