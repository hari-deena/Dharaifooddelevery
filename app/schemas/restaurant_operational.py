from pydantic import BaseModel, Field
from datetime import time
from typing import Optional,Literal

class RestaurantOperationalDetailsSchema(BaseModel):
    operational_id: Optional[int] = Field(None, description="Auto-generated ID (for response)")
    restaurant_id: int = Field(..., gt=0, description="Valid restaurant ID")
    estimated_delivery_time: Optional[str] = Field(None, max_length=50)
    delivery_charges_per_km: float = Field(0.0, ge=0.0)
    opening_time: time = Field(..., description="Opening time in HH:MM:SS format")
    closing_time: time = Field(..., description="Closing time in HH:MM:SS format")
    is_open: bool = Field(True)
    
    

class RestaurantIsOpenDetailsSchema(BaseModel):
    is_open: Literal[True, False]