from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    shop_id: int = Field(gt=0, description="Must be a positive integer")
    menu_id: int = Field(gt=0, description="Must be a positive integer")
    quantity: int = Field(gt=0, description="Must be a positive integer")

class OrderPayload(BaseModel):
    user_id: int = Field(gt=0, description="Must be a positive integer")
    total_amount: float = Field(ge=0, description="Must be a non-negative number (e.g., 0 or positive)")
    items: List[Item] = Field(min_length=1, description="At least one item is required")