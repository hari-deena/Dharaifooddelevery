from pydantic import BaseModel, Field, validator
from typing import List, Optional


class MenuSchema(BaseModel):
    menu_id: Optional[int] = Field(None, description="ID of the menu (optional, must be integer if provided)")
    restaurant_id: int = Field(..., description="ID of the restaurant")
    item_name: str = Field(..., min_length=2, max_length=255, description="Name of the dish")
    description: Optional[str] = Field(None, max_length=500, description="Dish description")
    price: float = Field(..., gt=0, description="Original price of the dish")
    discount_price: Optional[float] = Field(None, ge=0, description="Discounted price if any")
    is_available: bool = Field(True, description="Availability status of the dish")

    # category → list of category IDs
    category_id: int = Field(..., description="ID of the restaurant")

    veg_nonveg: str = Field(..., description="Dish type: VEG or NONVEG")
    preparation_time: Optional[int] = Field(None, ge=1, le=240, description="Preparation time in minutes")
    # menu_images: Optional[List[str]] = Field(None, description="List of image URLs for the menu item")
    
    @validator("menu_id")
    def validate_menu_id(cls, v):
        if v is not None and not isinstance(v, int):
            raise ValueError("menu_id must be an integer")
        return v

    @validator("veg_nonveg")
    def validate_veg_nonveg(cls, value):
        if value.upper() not in ["VEG", "NONVEG"]:
            raise ValueError("veg_nonveg must be either 'VEG' or 'NONVEG'")
        return value.upper()

    @validator("discount_price")
    def validate_discount_price(cls, v, values):
        if v is not None and "price" in values and v > values["price"]:
            raise ValueError("Discount price cannot be greater than the original price")
        return v

    # @validator("category")
    # def validate_category_ids(cls, v):
    #     if not all(isinstance(i, int) and i > 0 for i in v):
    #         raise ValueError("All category IDs must be positive integers")
    #     return v
