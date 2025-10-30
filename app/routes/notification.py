from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database_config import get_db
from app.services import notification
from app.schemas.notification import  FCMTokenRequest, FCMTokenQuery
from typing import Optional
from ..utils.response_handling import bad_request_response
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from ..routes.user import verify_token

user_router = APIRouter()



# Adds or updates the FCM token for a specific customer in the database.
@user_router.post("/fcm_token")
async def add_or_update_fcm_tokens(
    data: FCMTokenRequest,
    db: Session = Depends(get_db),
    user_data: str = Depends(verify_token)  
    
    
):
    return await notification.add_or_update_fcm_token(user_data, data, db)







# @notification_router.get("/notification")
# async def get_notification(
#     customer_id: Optional[int] = Query(None, description="ID of the customer"),
#     venue_id: Optional[int] = Query(None, description="ID of the venue"),
#     flag: Optional[bool] = Query(False, description="flag using get the specifig data."),
    
#     db: Session = Depends(get_db)
# ):
#     try:
#         data = NotificationQueryParams(customer_id=customer_id, venue_id=venue_id, flag=flag)
#     except ValidationError as ve:
#         # Extract only the custom message from the error list
#         first_error_msg = ve.errors()[0]['msg']
#         return bad_request_response(first_error_msg)
#     return await notification.get_notifications(data.customer_id, data.venue_id, data.flag, db)


# # Updates the view and count status of one or more notifications based on the request data.
# @notification_router.put("/notification")
# async def update_notifications(
#     request: NotificationUpdateRequest,
#     db: Session = Depends(get_db)
# ):
#     return await notification.update_view_and_count_status(request, db)

# # Adds a new notification or updates an existing one based on the request data.
# @notification_router.post("/notification")
# async def add_or_update_notification(
#     data: NotificationRequest,
#     db: Session = Depends(get_db)
# ):
#     return await notification.add_or_update_notifications(data, db)

# # Sends a push notification using the provided data without interacting with the database.
# @notification_router.post("/push_notification")
# async def push_notifications(
#     data: PushNotificationRequest
#  ):
#     return await notification.push_notification(data)


# # Fetches the FCM token for a customer if a valid customer ID is provided.
# @notification_router.get("/fcm_token")
# async def get_fcm_tokens(
#     customer_id: Optional[int] = Query(None, description="Optional customer ID"),
#     db: Session = Depends(get_db)
    
# ):
#     # Validate using schema
#     try:
#         validated_query = FCMTokenQuery(customer_id=customer_id)
#     except ValidationError:
#         return bad_request_response("Invalid customer id. It must be greater than 0 if provided.")

#     return await notification.get_fcm_token(customer_id, db)



# # Updates the view and count status of one or more notifications based on the request data.
# @notification_router.put("/turf_notification")
# async def update_turf_notification(
#     request: TurfNotificationUpdateRequest,
#     db: Session = Depends(get_db)
# ):
#     return await notification.update_turf_notifications(request, db)