from fastapi import APIRouter, UploadFile, Depends,Form, File, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database_config import get_db
from app.services import menu
from typing import Optional, List
from ..utils.response_handling import bad_request_response, handle_unauthorized_error
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from ..schemas.menu import MenuSchema 
from app.core.logger_config import configure_logger
logger = configure_logger('justplay')
from ..utils.response_handling import CustomAuthException
from .user import verify_token


menu_router = APIRouter()



@menu_router.post("/add_menu")
async def add_menus(
    shop_id: int = Form(...),
    item_name: str = Form(...),
    description: str = Form(...),
    price: float = Form(0.0),
    discount_price: float = Form(0.0),
    is_available: bool = Form(...),
    category_id: int = Form(...),  
    veg_nonveg: str = Form(...),  
    preparation_time : int = Form(...),
    menu_images: Optional[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    """
    Add a new restaurant (via form-data)
    """
    try:

        menu_data = MenuSchema(
            shop_id=shop_id,
            item_name=item_name,
            description=description,
            price=price,
            discount_price=discount_price,
            is_available=is_available,
            category_id=category_id,
            veg_nonveg=veg_nonveg,
            preparation_time=preparation_time,
            # menu_images=menu_images,
        )

        
        return await menu.add_menus(menu_data,menu_images,user_data, db)
        

    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        print("-----------------------> ")
        return bad_request_response(first_error_msg)





@menu_router.post("/update_menu/{menu_id}")
async def update_menus(
    menu_id: int,
    shop_id: int = Form(...),
    item_name: str = Form(...),
    description: str = Form(...),
    price: float = Form(0.0),
    discount_price: float = Form(0.0),
    is_available: bool = Form(...),
    category_id: int = Form(...),  
    veg_nonveg: str = Form(...),  
    preparation_time : int = Form(...),
    menu_images: Optional[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    """
    Add a new restaurant (via form-data)
    """
    try:

        menu_data = MenuSchema(
            menu_id=menu_id,
            shop_id=shop_id,
            item_name=item_name,
            description=description,
            price=price,
            discount_price=discount_price,
            is_available=is_available,
            category_id=category_id,
            veg_nonveg=veg_nonveg,
            preparation_time=preparation_time,
            # menu_images=menu_images,
        )

        
        return await menu.update_menus(menu_data,menu_images,user_data, db)
        

    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)




@menu_router.get("/get_menu")
async def get_menus(
    restaurant_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    item_name : Optional[str] = Query(None, description="restaurant id using get feedback"),
    category_id : Optional[int] = Query(None, description="restaurant id using get feedback"),
    veg_nonveg : Optional[str] = Query(None, description="restaurant id using get feedback"),

    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  # <-- Token auth dependency
    
):
    try:
        return await menu.get_menus(restaurant_id, item_name, category_id, veg_nonveg, user_data, db)
        
    except ValidationError as ve:
        # Extract only the custom message from the error list
        first_error_msg = ve.errors()[0]['msg']
        return bad_request_response(first_error_msg)
