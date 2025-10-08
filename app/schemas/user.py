import re
from pydantic import BaseModel, field_validator, ValidationError




class UserSchema(BaseModel):
    user_name: str
    mobile_number: str
    role_id: int  # Only accepts 1, 2, or 3

    @field_validator('user_name')
    @classmethod
    def validate_user_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('user_name cannot be empty')
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('user_name must contain only alphabetic characters and spaces')
        return v

    @field_validator('mobile_number')
    @classmethod
    def validate_mobile_number(cls, v: str) -> str:
        pattern = r'^\+91\d{10}$'
        if not re.match(pattern, v):
            raise ValueError('mobile_number must start with +91 followed by exactly 10 digits')
        return v

    @field_validator('role_id')
    @classmethod
    def validate_role_id(cls, v: int) -> int:
        allowed_ids = {1, 2, 3}
        if v not in allowed_ids:
            raise ValueError(f'role_id must be one of {list(allowed_ids)}, got {v}')
        return v
    

class LoginUserSchema(BaseModel):
    mobile_number: str

    @field_validator('mobile_number')
    @classmethod
    def validate_mobile_number(cls, v: str) -> str:
        pattern = r'^\+91\d{10}$'
        if not re.match(pattern, v):
            raise ValueError('mobile_number must start with +91 followed by exactly 10 digits')
        return v
    
    
class UpdateUserSchema(BaseModel):
    user_name: str
    
    @field_validator('user_name')
    @classmethod
    def validate_user_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('user_name cannot be empty')
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('user_name must contain only alphabetic characters and spaces')
        return v
    

    