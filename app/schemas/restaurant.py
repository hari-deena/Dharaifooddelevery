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










from pydantic import BaseModel, Field, validator
import re
from typing import Optional

class RestruntShopCreateSchema(BaseModel):
    shop_id: Optional[int] = Field(None, description="Unique ID of the shop")
    
    shop_name: str = Field(..., min_length=1, max_length=255)
    shop_address: str = Field(..., min_length=5)
    
    # GST: Format like 22AAAAA0000A1Z5 (15 chars: 2 digits + 10 alphanumeric + 1 digit + 1 alpha + 1 digit)
    GST_license: Optional[str] = Field(None, max_length=50)
    
    # FSSAI: 14-digit numeric string
    fssai: Optional[str] = Field(None, max_length=14)
    
    # PAN: 10 characters (5 alpha + 4 digits + 1 alpha)
    pan: Optional[str] = Field(None, max_length=10)
    
    bank_name: str = Field(..., min_length=2, max_length=100)
    account_number: str = Field(..., min_length=9, max_length=50)
    ifsc_code: str = Field(..., min_length=11, max_length=11)

    @validator('GST_license')
    def validate_gst(cls, v):
        if v is None:
            return v
        if not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$', v):
            raise ValueError('Invalid GST format. Example: 22AAAAA0000A1Z5')
        return v.upper()

    @validator('fssai')
    def validate_fssai(cls, v):
        if v is None:
            return v
        if not v.isdigit() or len(v) != 14:
            raise ValueError('FSSAI must be a 14-digit numeric string')
        return v

    @validator('pan')
    def validate_pan(cls, v):
        if v is None:
            return v
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', v):
            raise ValueError('Invalid PAN format. Example: ABCDE1234F')
        return v.upper()

    @validator('ifsc_code')
    def validate_ifsc(cls, v):
        if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', v):
            raise ValueError('Invalid IFSC code. Format: XXXX0XXXXXX (e.g., SBIN0002499)')
        return v.upper()

    @validator('account_number')
    def validate_account_number(cls, v):
        if not v.replace(' ', '').replace('-', '').isdigit():
            raise ValueError('Account number must contain only digits, spaces, or hyphens')
        return v

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "shop_name": "Tasty Bites",
    #             "shop_address": "123 Food Street, Mumbai, Maharashtra",
    #             "GST_license": "27AABCCDDEEFFG",
    #             "fssai": "12345678901234",
    #             "pan": "ABCDE1234F",
    #             "bank_name": "State Bank of India",
    #             "account_number": "12345678901",
    #             "ifsc_code": "SBIN0002499"
    #         }
    #     }
        
        
        
class ShopVerificationRequest(BaseModel):
    shop_id: int = Field(..., description="Unique ID of the shop")
    verification_status: str = Field(..., description="Status must be either APPROVED or REJECTED")
    reason: Optional[str] = Field(None, description="Reason for rejection or approval (optional)")

    @validator('verification_status')
    def validate_status(cls, value):
        allowed_status = {'APPROVED', 'REJECTED'}
        if value not in allowed_status:
            raise ValueError("verification_status must be either 'APPROVED' or 'REJECTED'")
        return value