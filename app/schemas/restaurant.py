import re
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
import json

class RestaurantSchema(BaseModel):
    restaurant_id: Optional[int] = None  # Optional, must be int if provided
    restaurant_name: str
    address: str
    vat_tax: float
    cuisine: str
    food_type: str
    zone: str
    latitude: float
    longitude: float
    delivery_type: str
    restaurant_phone: Optional[str] = None  # ✅ optional
    
    
    # ✅ Optional restaurant_id validation
    @field_validator("restaurant_id")
    def validate_restaurant_id(cls, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("restaurant_id must be an integer if provided")
        return value

    # ✅ Non-empty string validation
    @field_validator("restaurant_name", "address", "zone", "delivery_type", "food_type")
    def non_empty_string(cls, value, field):
        if not value or not value.strip():
            raise ValueError(f"{field.name} cannot be empty")
        return value.strip()

    # ✅ Float validation
    @field_validator("vat_tax", "latitude", "longitude")
    def must_be_float(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be empty")
        if not isinstance(value, (float, int)):
            raise ValueError(f"{field.name} must be a float")
        return float(value)

    # ✅ Cuisine validation (must be non-empty list of ints)
    # @field_validator("cuisine", mode="before")
    # def validate_cuisine(cls, value):
    #     # If value comes as string from form-data → parse it
    #     if isinstance(value, str):
    #         try:
    #             value = json.loads(value)
    #         except Exception:
    #             raise ValueError("cuisine must be a valid JSON list of integers")

    #     if not value or not isinstance(value, list):
    #         raise ValueError("cuisine must be a non-empty list")

    #     if not all(isinstance(v, int) for v in value):
    #         raise ValueError("cuisine list must contain only integers")

    #     return value

    # ✅ Phone number validation
    # @field_validator("restaurant_phone")
    # def validate_phone(cls, value):
    #     if value is None or value.strip() == "":
    #         return value  # allow empty
    #     phone_pattern = re.compile(r"^\d{7,15}$")
    #     if not phone_pattern.match(value):
    #         raise ValueError("restaurant_phone must be 7–15 digits only")
    #     return value
    
    @field_validator('restaurant_phone')
    @classmethod
    def validate_mobile_number(cls, v: str) -> str:
        pattern = r'^\+91\d{10}$'
        if not re.match(pattern, v):
            raise ValueError('mobile_number must start with +91 followed by exactly 10 digits')
        return v
