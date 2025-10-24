from pydantic import BaseModel, Field, StringConstraints
from typing import Optional, Annotated

class UserAddress(BaseModel):
    address_id: Optional[int] = Field(None)
    delivery_details: Optional[str] = Field(None, max_length=255)
    address_details: Optional[str] = Field(None, max_length=500)
    receiver_name: Optional[str] = Field(None, max_length=100)
    receiver_phone: Optional[
        Annotated[str, StringConstraints(pattern=r'^\d{10,15}$')]
    ] = Field(None, description="Receiver phone number (10–15 digits)")
    address_save_as: Optional[str] = Field(None, max_length=50)
    # is_active: Optional[bool] = Field(None)
