from fastapi import APIRouter, UploadFile, Depends,Form, File, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database_config import get_db
from app.services import restaurant
from typing import Optional, List
from ..utils.response_handling import bad_request_response, handle_unauthorized_error
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from ..schemas.restaurant import RestaurantSchema , RestruntShopCreateSchema, ShopVerificationRequest
from app.core.logger_config import configure_logger
logger = configure_logger('justplay')
from ..utils.response_handling import CustomAuthException
from .user import verify_token


restaurant_router = APIRouter()






@restaurant_router.post("/add_restaurant")
async def add_restaurant(
    restaurant_name: str = Form(...),
    address: str = Form(...),
    vat_tax: float = Form(0.0),
    cuisine: str = Form(...),  
    food_type: str = Form(...),
    zone: Optional[str] = Form(...),
    latitude: Optional[float] = Form(...),
    longitude: Optional[float] = Form(...),
    restaurant_phone: Optional[str] = Form(...),
    delivery_type: str = Form(...),
    logo: Optional[UploadFile] = File(...),
    restaurant_image: Optional[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    """
    Add a new restaurant (via form-data)
    """
    try:

        restaurant_data = RestaurantSchema(
            restaurant_name=restaurant_name,
            address=address,
            vat_tax=vat_tax,
            cuisine=cuisine,
            food_type=food_type,
            zone=zone,
            latitude=latitude,
            longitude=longitude,
            restaurant_phone=restaurant_phone,
            delivery_type=delivery_type,
        )

        
        return await restaurant.add_restaurant(restaurant_data,logo,restaurant_image,user_data, db)
        

    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)



@restaurant_router.put("/update_restaurant/{restaurant_id}")
async def update_restaurant(
    restaurant_id : int ,
    restaurant_name: str = Form(...),
    address: str = Form(...),
    vat_tax: float = Form(0.0),
    cuisine: str = Form(...),  
    food_type: str = Form(...),
    zone: Optional[str] = Form(...),
    latitude: Optional[float] = Form(...),
    longitude: Optional[float] = Form(...),
    restaurant_phone: Optional[str] = Form(...),
    delivery_type: str = Form(...),
    logo: Optional[UploadFile] = File(...),
    restaurant_image: Optional[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    """
    Add a new restaurant (via form-data)
    """
    try:

        restaurant_data = RestaurantSchema(
            restaurant_id=restaurant_id,
            restaurant_name=restaurant_name,
            address=address,
            vat_tax=vat_tax,
            cuisine=cuisine,
            food_type=food_type,
            zone=zone,
            latitude=latitude,
            longitude=longitude,
            restaurant_phone=restaurant_phone,
            delivery_type=delivery_type,
        )

        
        return await restaurant.update_restaurant(restaurant_data,logo,restaurant_image,user_data, db)
        

    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)





@restaurant_router.get("/get_restaurant")
async def get_restaurant(
    restaurant_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await restaurant.get_restaurant(restaurant_id,user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)








# ------------------------------------------------------------------------- newly worked -----------------------------------------------


@restaurant_router.post("/add_shop")
async def add_shop(
    request: RestruntShopCreateSchema,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await restaurant.add_shop(request, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)
    
    
    
@restaurant_router.get("/get_shop")
async def get_restaurant(
    shop_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    verification_status : Optional[str] = Query(None, description="restaurant verification_status  using get feedback"),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await restaurant.get_shop(shop_id,verification_status,user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)


@restaurant_router.post("/shop_verification")
async def shop_verification(
    request: ShopVerificationRequest,
    db: Session = Depends(get_db)
    
):
    try:
        return await restaurant.shop_verification(request, db)
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)
    
    
    
@restaurant_router.put("/add_shop_imaes")
async def add_shop_imaes(
    shop_id: int = Form(...),
    logo: Optional[UploadFile] = File(...),
    shop_image: Optional[UploadFile] = File(...),
    banner: Optional[UploadFile] = File(...),
    db: Session = Depends(get_db),
    # user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    """
    Add a new restaurant (via form-data)
    """
    try:

        
        return await restaurant.add_shop_imaes(shop_id,logo,shop_image,banner, db)
        

    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)
