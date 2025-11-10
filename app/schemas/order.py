from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Item(BaseModel):
    shop_id: int = Field(gt=0, description="Must be a positive integer")
    menu_id: int = Field(gt=0, description="Must be a positive integer")
    quantity: int = Field(gt=0, description="Must be a positive integer")

class OrderPayload(BaseModel):
    # user_id: int = Field(gt=0, description="Must be a positive integer")
    total_amount: float = Field(ge=0, description="Must be a non-negative number (e.g., 0 or positive)")
    items: List[Item] = Field(min_length=1, description="At least one item is required")
    
    
    
    
class RestaurantStatusEnum(str, Enum):
    REJECTED = "REJECTED"
    PREPARING = "PREPARING"
    READY_FOR_PICKUP = "READY_FOR_PICKUP"
    ACCEPTED = 'ACCEPTED'

class RestaurantOrderStatusRequest(BaseModel):
    shop_id: int = Field(..., gt=0, description="Unique ID of the shop")
    order_id: int = Field(..., gt=0, description="Unique ID of the order")
    rest_status: RestaurantStatusEnum = Field(..., description="Current status of the restaurant order")
