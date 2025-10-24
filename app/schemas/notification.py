from pydantic import BaseModel, model_validator, Field, field_validator
from enum import StrEnum
from typing import List, Optional, Literal
from fastapi import HTTPException
from ..utils import config
from pydantic import BaseModel
from typing import List


  
# Validates that the FCM token is a non-empty string when saving or updating a device token. 
class FCMTokenRequest(BaseModel):
    fcm_token: str = Field(..., description="Firebase Cloud Messaging token")

    @field_validator('fcm_token', mode='before')
    @classmethod
    def validate_token_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("FCM token must not be empty.")
        return v
    
# Optionally validates a customer ID, ensuring it is greater than 0 if provided.
class FCMTokenQuery(BaseModel):
    customer_id: Optional[int] = Field(
        None,
        gt=0,
        description="Optional customer ID. If provided, must be greater than 0"
    )
    
    


# # Validates the structure and logical combinations of data used to create or update notifications, based on a flag.
# class NotificationRequest(BaseModel):
#     booking_source: int
#     customer_id: Optional[int] = None
#     turf_id : Optional[int] = None
#     venue_id : Optional[int] = None
#     booking_id: Optional[int] = None
#     booking_ids: Optional[List[int]] = None
#     flag: Optional[Literal['True', 'False']] = 'True'

#     @model_validator(mode='after')
#     def check_valid_combinations(cls, values):
#         booking_source = values.booking_source
#         customer_id = values.customer_id
#         turf_id = values.turf_id
#         venue_id = values.venue_id
#         booking_id = values.booking_id
#         booking_ids = values.booking_ids
#         flag = values.flag

#         # Valid case 1: flag = 'False', booking_source, booking_id, customer_id are present, booking_ids is None
#         if (
#             flag == config.status_false
#             and booking_source 
#             and booking_id 
#             and customer_id 
#             and turf_id
#             and venue_id
#             and not booking_ids 
#         ):
#             return values

#         # Valid case 2: flag = config.status_true, booking_source and booking_ids present, booking_id and customer_id None
#         if (
#             flag == config.status_true
#             and booking_source is not None
#             and booking_ids is not None and len(booking_ids) > config.index_zero
#             and booking_id is None
#             and customer_id is None
#             and turf_id is None
#             and venue_id is None
#         ):
#             return values

#         raise HTTPException(
#         status_code=422,
#         detail={
#             "status": False,
#             "message": "Invalid data combination. Must match one of the valid cases."
#         }
#     )
        

    
# # Defines constant string values (CONFIRM, CANCEL, SCHEDULE) for the flag field used in push notifications
# class FlagEnum(StrEnum):
#     CONFIRM = config.status_CONFIRM
#     CANCEL = config.status_CANCEL
#     SCHEDULE = config.status_SCHEDULE

# # Validates push notification input data, ensuring required fields are numeric strings and optional 
# # IDs are valid if provided.
# class PushNotificationRequest(BaseModel):
#     token: str = Field(..., description="FCM device token")
#     body: str = Field(..., description="Notification message body")
#     booking_id: str = Field(..., description="ID of the booking")
#     booking_source: str = Field(..., description="Source identifier for the booking")

#     # Optional fields
#     user_id: Optional[str] = Field(None, description="ID of the user receiving the notification")
#     notification_id: Optional[str] = Field(None, description="ID for the notification record")
#     flag: Optional[FlagEnum] = Field(None, description="Status flag - CONFIRM, CANCEL, or SCHEDULE")

#     @field_validator("booking_id", "booking_source")
#     def validate_required_ids(cls, v: str) -> str:
#         if not v.isdigit():
#             raise ValueError(f"{v} must be a numeric string")
#         return v

#     @field_validator("user_id", "notification_id")
#     def validate_optional_int_fields(cls, v: Optional[str]) -> Optional[str]:
#         if v is not None and not v.isdigit():
#             raise ValueError(f"{v} must be a numeric string if provided")
#         return v
    
# # Ensures that notification IDs are not empty and the flag is a boolean when updating view or count statuses.
# class NotificationUpdateRequest(BaseModel):
#     notification_id: List[int]
#     flag: bool

#     @field_validator("notification_id")
#     @classmethod
#     def validate_notification_id(cls, value):
#         if not value:
#             raise ValueError('notification_id must not be empty')
#         return value

#     @field_validator('flag', mode='before')
#     @classmethod
#     def validate_flag(cls, value):
#         if isinstance(value, bool):
#             return value
#         raise ValueError("flag must be a boolean: true or false only")
  

# class NotificationQueryParams(BaseModel):
#     customer_id: Optional[int] = None
#     venue_id: Optional[int] = None
#     flag: Optional[bool]  = False

#     @model_validator(mode='after')  # For Pydantic v2
#     def validate_either_or(self):
#         if self.customer_id is None and self.venue_id is None:
#             raise ValueError("Either customer_id or venue_id must be provided.")
#         if self.customer_id is not None and self.venue_id is not None:
#             raise ValueError("Provide only one of customer_id or venue_id, not both.")
#         return self
    
#     @field_validator("flag", mode="before")
#     def validate_flag(cls, value):
#         if value not in [True, False, None]:
#             raise ValueError("flag must be either true or false.")
#         return value
    
    
    
    
# class TurfNotificationUpdateRequest(BaseModel):
#     venue_id: int
#     turf_owner_notification_id: int

#     @field_validator('venue_id')
#     def validate_venue_id(cls, v):
#         if v is None:
#             raise ValueError("venue_id cannot be null.")
#         if v < 0:
#             raise ValueError("venue_id cannot be negative.")
#         return v

#     @field_validator('turf_owner_notification_id')
#     def validate_notification_id(cls, v):
#         if v is None:
#             raise ValueError("turf_owner_notification_id cannot be null.")
#         if v < 0:
#             raise ValueError("turf_owner_notification_id cannot be negative.")
#         return v