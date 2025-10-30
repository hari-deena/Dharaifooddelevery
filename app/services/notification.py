from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
from app.query.queries import get_filtered_fields, get_first_record, insert_record, update_records
from app.utils.email_templates import generate_booking_confirmation, generate_booking_cancellation, generate_turf_inactive_cancellation, generate_booking_completed, generate_turf_booking_confirmation_nad_cancelation
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import  FcmToken
from app.core.logger_config import configure_logger
from app.utils import config
from app.utils.response_message import notification_response_message
from firebase_admin import messaging
import asyncio

logger = configure_logger('justplay')



# This function inserts or updates an FCM token for a user after validating their existence, 
# handling both insert and update flows with proper error handling and logging.
async def add_or_update_fcm_token(user_data, data, db):
    try:    
        
        customer_id = user_data["user_id"]
        
        logger.info(f"Customer id: {customer_id}, FCM token: {data.fcm_token}")
        
        
        # Check if user already there in fcm token table or not 
        existing_token = get_first_record(
                db=db,
                model=FcmToken,
                filters=[FcmToken.user_id == customer_id]
            )
        
        # logger.info("Get fcm table to user_id: %s",existing_token)
        logger.info("Fetched FCM token record for user_id: %s", existing_token.user_id if existing_token else "No record found")

        if existing_token is False:
            logger.error("An error occurred while checking if the FCM token exists.")
            return server_error_response(notification_response_message('Error','fcm_token_check_error'))
        
        # Update flow for fcm token
        if existing_token:
            logger.info("Starting FCM token update.")
            token_result = update_records(
                db=db,
                model=FcmToken,
                filter_condition=(FcmToken.user_id == customer_id),
                update_data={
                    "fcm_token": data.fcm_token,
                    "updated_at": datetime.utcnow()
                }
            )
        # Insert flow for fcm token
        else:
            logger.info("Starting FCM token insert.")
            token_result = insert_record(
                db=db,
                model=FcmToken,
                data={
                    "user_id": customer_id,
                    "fcm_token": data.fcm_token
                }
            )
        
        # logger.info("FCM token add or update result: %s",token_result)
        logger.info("FCM token operation completed. Result: %s", token_result)

        if not token_result:
            logger.error("Failed to insert or update the FCM token in the database.")
            return server_error_response(notification_response_message('Error','fcm_token_upsert_failed'))
        
        logger.info("Successfully insert or update the fcm token.")
        return handle_success(notification_response_message('Success','fcm_token_upsert_success'))
    
    except Exception as unexpected_error:
        logger.exception(f"Unexpected error: {str(unexpected_error)}")
        db.rollback()
        return server_error_response(f"Unexpected error: {str(unexpected_error)}")




# # Converts a UTC datetime string to IST datetime string in the same format.
# def convert_utc_to_ist(time_str: str) -> str:
#     """
#     Convert UTC datetime string to IST datetime string.
    
#     Args:
#         time_str (str): UTC datetime in '%Y-%m-%d %H:%M:%S' format.

#     Returns:
#         str: IST datetime in '%Y-%m-%d %H:%M:%S' format.
#     """
#     original_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
#     utc_dt = original_dt.replace(tzinfo=ZoneInfo("UTC"))
#     ist_dt = utc_dt.astimezone(ZoneInfo("Asia/Kolkata"))
#     return ist_dt.strftime("%Y-%m-%d %H:%M:%S")    


# # Processes raw notification data into a formatted list with messages, timestamps, and 
# # a count of unread notifications
# def turf_data_convert(notification_data):
#     result = []
#     notification_count = config.index_zero
    
#     for row in notification_data:
#         if row["count_status"] == config.status_true:
#             notification_count += config.index_one
            
#         # updated_at = row["updated_time"]
#         # if isinstance(updated_at, str):
#         #         dt = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
#         #         updated_at = dt.strftime("%d %b, %Y | %H:%M")
                
#         updated_at = row["updated_time"]
#         if isinstance(updated_at, str):
#             dt = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
#             updated_at = dt.strftime("%d %b, %Y | %I:%M %p") 
                
#         data = {
#             "turf_owner_notification_id": row["turf_owner_notification_id"],
#             "customer_id": row["customer_id"],
#             "booking_id": row["booking_id"],
#             "booking_source": row["booking_source"],
#             "view_status": row["view_status"],
#             "count_status": row["count_status"],
#             "first_name" : row["first_name"],
#             "last_name" : row["last_name"],
#             "profile_url" : row["profile_url"],
#             "mobile_number" : row["mobile_number"],
#             "updated_time" : updated_at
            
#         }
        
#         turf_name = row["turf_name"]

#         start_time = row["start_time"]
#         end_time = row["end_time"]
#         # total_amount = row["total_amount"]
#         # cancellation_amount = row["cancellation_amount"]

#         # Format date and time for the message
#         # formatted_date = start_time.strftime("%B %d, %Y")
#         formatted_start_time = start_time.strftime("%I:%M %p")
#         formatted_end_time = end_time.strftime("%I:%M %p")
   
#         # Generate message based on source
#         data["message"] = generate_turf_booking_confirmation_nad_cancelation(turf_name, formatted_start_time, formatted_end_time)
        
        
#         # if row["booking_source"] == config.index_one:
#         #     message = generate_turf_booking_confirmation_nad_cancelation(turf_name, formatted_start_time, formatted_end_time)
#         # else :
#         #     message = generate_turf_booking_cancellation(formatted_start_time, formatted_end_time)
       
#         notification_time = convert_utc_to_ist(row["created_time"])
#         data["notification_time"] = notification_time
#         # data["message"] = message

#         result.append(data)

#     # Final response structure
#     response = {
#         "notifications": result,
#         "count": notification_count
#     }

#     return response


# def customer_data_convert(notification_data):
#     result = []
#     notification_count = config.index_zero
    
#     for row in notification_data:
#         if row["count_status"] == config.status_true:
#             notification_count += config.index_one

#         data = {
#             "notification_id": row["notification_id"],
#             "customer_id": row["customer_id"],
#             "booking_id": row["booking_id"],
#             "booking_source": row["booking_source"],
#             "view_status": row["view_status"],
#             "count_status": row["count_status"]
#         }

#         start_time = row["start_time"]
#         end_time = row["end_time"]
#         total_amount = row["total_amount"]
#         cancellation_amount = row["cancellation_amount"]

#         # Format date and time for the message
#         formatted_date = start_time.strftime("%B %d, %Y")
#         formatted_start_time = start_time.strftime("%I:%M %p")
#         formatted_end_time = end_time.strftime("%I:%M %p")

#         # Generate message based on source
#         if row["booking_source"] == config.index_one:
#             message = generate_booking_confirmation(formatted_date, formatted_start_time, formatted_end_time, total_amount)
#         elif row["booking_source"] == config.index_two:
#             message = generate_booking_cancellation(formatted_date, formatted_start_time, formatted_end_time, cancellation_amount)
#         elif row["booking_source"] == config.index_three:
#             message = generate_booking_completed(formatted_date, formatted_start_time, formatted_end_time, cancellation_amount)
#         else:
#             message = generate_turf_inactive_cancellation(formatted_date, formatted_start_time, formatted_end_time, cancellation_amount)

#         notification_time = convert_utc_to_ist(row["created_time"])
#         data["notification_time"] = notification_time
#         data["message"] = message

#         result.append(data)

#     # Final response structure
#     response = {
#         "notifications": result,
#         "count": notification_count
#     }

#     return response


# # Fetches and returns notifications for a given customer after validating the user 
# # and formatting the response data.
# # async def get_notifications(customer_id, db):
# #     try:    
        
# #         logger.info("Customer id: %s",customer_id)
        
# #         # Check if user exists
# #         user = get_first_record(
# #             db=db,
# #             model=User,
# #             filters=[
# #                 User.user_id == customer_id,
# #                 User.role_id == config.user_role_id
# #             ]
# #         )
        
# #         if user == False:
# #             logger.error("An error occurred while querying the user from the database.")
# #             return server_error_response(notification_response_message('Error','user_query_error'))
            
# #         elif not user:
# #             logger.error("User is not found.")
# #             return bad_request_response(notification_response_message('Error','invalid_data'))
        
# #         logger.info("User check result: %s",user.user_id)
        
# #         notification_data = get_notifications_by_customer(customer_id, db)
# #         logger.info("Notification data: %s",notification_data)
        
# #         result = data_convert(notification_data)
# #         message = notification_response_message('Success','get_success') if result else notification_response_message('Success','no_data')
        
# #         logger.info("Response msg: %s",message)

# #         return handle_success_with_data(message,result)
    
# #     except Exception as unexpected_error:
# #         logger.exception(f"Unexpected error: {str(unexpected_error)}")
# #         return server_error_response(f"Unexpected error: {str(unexpected_error)}")
 

# async def get_notifications(customer_id, venue_id, flag,  db):
#     try:    
        
#         logger.info("Customer ID: %s, Venue ID: %s, Flag: %s", customer_id, venue_id, flag)

#         # Determine context
#         if not flag:
#             context = {
#                 "model": User,
#                 "filters": [User.user_id == customer_id, User.role_id == config.user_role_id],
#                 "get_notifications": get_notifications_by_customer,
#                 "convert_func": customer_data_convert,
#                 "entity_id": customer_id
#             }
#         else:
#             print("----------------> ")
#             context = {
#                 "model": Venue,
#                 "filters": [Venue.venue_id == venue_id],
#                 "get_notifications": get_notifications_by_turf,
#                 "convert_func": turf_data_convert,
#                 "entity_id": venue_id
#             }

#         # Validate entity existence
#         entity = get_first_record(db=db, model=context["model"], filters=context["filters"])
#         if entity is False:
#             logger.error("Error while querying the entity from the database.")
#             return server_error_response(notification_response_message('Error', 'user_query_error'))

#         if not entity:
#             logger.error("Entity not found.")
#             return bad_request_response(notification_response_message('Error', 'invalid_data'))

#         logger.info("Entity found: %s", entity)

#         # Fetch and convert notifications
#         notifications = context["get_notifications"](context["entity_id"], db)
#         logger.info("Raw Notification Data: %s", notifications)

#         result = context["convert_func"](notifications)
#         message = notification_response_message('Success', 'get_success') if result else notification_response_message('Success', 'no_data')

        
#         # flag = False ->
        
        
#         # notification_data = get_notifications_by_customer(customer_id, db)
#         # logger.info("Notification data: %s",notification_data)
        
#         # result = customer_data_convert(notification_data)
#         # message = notification_response_message('Success','get_success') if result else notification_response_message('Success','no_data')
        
#         logger.info("Response msg: %s",message)

#         return handle_success_with_data(message,result)
    
#     except Exception as unexpected_error:
#         logger.exception(f"Unexpected error: {str(unexpected_error)}")
#         return server_error_response(f"Unexpected error: {str(unexpected_error)}")
 


# # This function inserts a new notification or updates existing ones based on the input flag, 
# # while handling duplicates, logging progress, and managing database transactions and errors.
# async def add_or_update_notifications(data, db):
#     try:
#         logger.info("Payload received for notification insertion: %s", data)
        
#         # Insert flow for notification
#         if data.flag == config.status_false: 
#             logger.info("Starting the notification insertion process.")
            
#             # check the data 
#             existing_booking = get_first_record(
#                 db,
#                 Notification,
#                 [
#                     Notification.booking_id == data.booking_id
#                 ]
#             )
                        
#             logger.info("Checking for existing booking entry: %s", existing_booking)
#             if existing_booking == False:
#                 logger.error("Error occurred while executing the user validation query.")
#                 return server_error_response("Error occurred while executing the user validation query.")
#             elif existing_booking:
#                 logger.error("Booking ID %s already exists. Skipping insertion.", data.booking_id)
#                 return bad_request_response(notification_response_message('Error','already_exist'))
#             common_params = {
#             "customer_id": data.customer_id,
#             "booking_id": data.booking_id,
#             "booking_source": data.booking_source,
#         }
            
#             # Insert notification fun call
#             new_notification = insert_record(db, Notification, common_params)
#             logger.info("Notification object prepared for insertion: %s", new_notification)
            
#             if not new_notification:
#                 logger.error("An error occurred while inserting the notification.")
#                 return server_error_response(notification_response_message('Error','insert_error'))
            
#             notification_id = new_notification.notification_id
#             logger.info("Notification inserted successfully with ID: %s", notification_id)
#             response_data = {"notification_id" : notification_id}
            
#             # Turf owner notification table to insert 
#             common_params.update({
#             "turf_id": data.turf_id,
#             "venue_id": data.venue_id,
#             "notification_id": notification_id
#         })
            
#             new_turf_notification = insert_record(db, TurfOwnerNotification, common_params)
#             logger.info("Insert turf owner notification result: %s",new_turf_notification)
#             if not new_turf_notification:
#                 logger.error("An error occurred while inserting the notification.")
#                 db.rollback()
#                 return server_error_response(notification_response_message('Error','insert_error'))
            
#             logger.info("Notification insertion completed successfully.")
#             return handle_success_with_data(notification_response_message('Success','insert_success'), response_data)
        
#         # Update flow for notification 
#         else:
#             logger.info("Starting the notification update process.")
            
#             # Update the Notification table
#             update_result = update_records(
#                 db=db,
#                 model=TurfOwnerNotification,
#                 filter_condition=TurfOwnerNotification.booking_id.in_(data.booking_ids),
#                 update_data={
#                     TurfOwnerNotification.view_status: config.status_true,
#                     TurfOwnerNotification.booking_source: data.booking_source
#                 }
#             )
#             logger.info("Updating notifications for booking IDs: %s that result: %s ", data.booking_ids, update_result)
            
#             if not update_result :
#                 logger.error("No matching records found or input data is invalid.")
#                 return bad_request_response(notification_response_message('Error','update_no_match'))
             
            
#             if data.booking_source == 2:
#                 # Update the turf owner Notification table
#                 update_result = update_records(
#                     db=db,
#                     model=Notification,
#                     filter_condition=Notification.booking_id.in_(data.booking_ids),
#                     update_data={
#                         Notification.view_status: config.status_true,
#                         Notification.booking_source: data.booking_source
#                     }
#                 )
#                 logger.info("Updating the turf notifications for booking IDs: %s that result: %s ", data.booking_ids, update_result)
                
#                 if not update_result :
#                     logger.error("No matching records found or input data is invalid.")
#                     db.rollback()
#                     return bad_request_response(notification_response_message('Error','update_no_match'))
                
            
#             logger.info("Successfully update the notification.") 
#             return handle_success(notification_response_message('Success','update_success'))
    
#     except Exception as unexpected_error:
#         logger.exception(f"Unexpected error: {str(unexpected_error)}")
#         db.rollback()
#         return server_error_response(f"Unexpected error: {str(unexpected_error)}")
    
    

# # Creates a push notification payload with common and conditional fields based on the 
# # notification type (confirm, cancel, or schedule).
# def generate_payload_data(data):
#     common_fields = {
#         "booking_id": str(data.booking_id),
#         "booking_source": str(data.booking_source),
#     }

#     if data.flag == config.status_CONFIRM:
#         logger.info("Sending confirmation notification.")
#         payload = {
#             **common_fields,
#             "user_id": str(data.user_id),
#             "notification_id": str(data.notification_id),
#         }
#     elif data.flag == config.status_CANCEL:
#         logger.info("Sending cancellation notification.")
#         payload = common_fields
#     else:
#         logger.info("Sending scheduled notification.")
#         payload = {
#             **common_fields,
#             "user_id": str(data.user_id),
#             "notification_id": str(data.notification_id),
#         }

#     return payload

# # Sends a push notification to a device using Firebase Cloud Messaging (FCM), based on the 
# # provided data and constructed payload.
# async def push_notification(data):
#     try:
#         logger.info("Retrieved data for push notification: %s", data)
        
#         token = data.token
#         body = data.body
        
#         # Generete paylod data 
#         data = generate_payload_data(data)
#         logger.info("Constructed payload for push notification: %s", data)
        
#         # check token if heare 
#         if token:
#             message = messaging.Message(
#                 notification=messaging.Notification(
#                     title=config.justplay,
#                     body=body,
#                 ),
#                 token=token,
#                 data=data
#             )
            
#             # send notification 
#             loop = asyncio.get_event_loop()
#             response = await loop.run_in_executor(None, messaging.send, message)
#             logger.info(f'Successfully sent message: {response}')
#         else:
#             logger.error("FCM token is missing in the request.")
#             return bad_request_response(notification_response_message('Error','fcm_token_missing'))
#         return handle_success(notification_response_message('Success','send_notification'))
    
#     except Exception as unexpected_error:
#         logger.exception(f"Unexpected error: {str(unexpected_error)}")
#         return server_error_response(notification_response_message('Error','send_notification_error'))


# # This function validates notification IDs and updates either their view status or count status 
# # based on a flag, handling missing records and database errors gracefully
# async def update_view_and_count_status(request, db):
#     try:
#         logger.info("The request data: %s",request)
        
#         notification_ids = request.notification_id
        
#         # check the data if present the table 
#         existing_ids = get_filtered_fields(
#             db, 
#             Notification, 
#             [Notification.notification_id], 
#             [Notification.notification_id.in_(notification_ids)]
#         )
#         logger.info("Get the notification ids: %s",existing_ids)
#         if not existing_ids:
#             logger.error("Invalid notification id.")
#             return bad_request_response("Invalid notification id.")
        
#         # Flatten list of tuples to just a list of IDs
#         existing_ids_set = {id_[config.index_zero] for id_ in existing_ids}
        
#         # Find missing IDs
#         missing_ids = set(notification_ids) - existing_ids_set
#         logger.info("Missing ids: %s",missing_ids)
#         if missing_ids:
#             logger.error(f"Invalid notification id: {sorted(missing_ids)}")
#             return bad_request_response(notification_response_message('Error','invalid_id'))

#         # flag variable using navigate operations
#         if request.flag == False:
#             logger.info("Starting the update view status flow.")
#             notification_id = request.notification_id[config.index_zero]
#             logger.info("Customer id: %s",notification_id)
#             filter_condition = (Notification.notification_id == notification_id)
#             update_data = {Notification.view_status: config.status_false}
            
#         else:
#             logger.info("Starting the update count status flow.")
            
#             notification_ids = request.notification_id
#             logger.info("Customer ids: %s",notification_ids)
#             filter_condition=Notification.notification_id.in_(notification_ids)
#             update_data={Notification.count_status: config.status_false}
         
#         # Update the data. 
#         rows_updated = update_records(
#             db=db,
#             model=Notification,
#             filter_condition=filter_condition,
#             update_data=update_data
#         )
        
#         logger.info("Update result check: %s",rows_updated)
#         if not rows_updated :
#             logger.error("A notification with this booking ID already exists.")
#             return server_error_response(notification_response_message('Error','already_exist'))

#         db.commit()
#         logger.info("Notification updated successfully.")
#         return handle_success(notification_response_message('Success','notification_update'))
    
#     except Exception as unexpected_error:
#         logger.exception(f"Unexpected error: {str(unexpected_error)}")
#         db.rollback()
#         return server_error_response(f"Unexpected error: {str(unexpected_error)}")



 
# # This function fetches FCM tokens for a given customer ID (if provided), validates the user, 
# # formats the response, and handles possible errors.
# async def get_fcm_token(customer_id, db):
#     try:    
#         # logger.info("Customer id: %s",customer_id)
#         logger.info("Fetching FCM tokens for Customer ID: %s", customer_id)
#         if customer_id:
#             # Check if user exists
#             user = get_first_record(
#                 db=db,
#                 model=User,
#                 filters=[
#                     User.user_id == customer_id,
#                     User.role_id == config.user_role_id
#                 ]
#             )
            
#             if user == False:
#                 logger.error("An error occurred while querying the user from the database.")
#                 return server_error_response(notification_response_message('Error','user_query_error'))
                
#             elif not user:
#                 logger.error("User is not found.")
#                 return bad_request_response(notification_response_message('Error','invalid_data'))
            
#             # logger.info("User check result: %s",user.user_id)
#             logger.info("User found with User ID: %s", user.user_id)
            
        
#         # Get users fcm token
#         result = get_filtered_fields(
#                 db,
#                 UserFCMToken,
#                 [UserFCMToken.fcm_token_id, UserFCMToken.user_id, UserFCMToken.fcm_token],
#                 [UserFCMToken.user_id == customer_id] if customer_id else []
#             )
        
#         if result is False:
#             logger.error("An error occurred while fetching FCM tokens.")
#             return server_error_response(notification_response_message('Error','error_fetching_fcm'))
        
#         # generate msg format 
#         msg = notification_response_message('Success','success_message_fcm') if result else notification_response_message('Success','no_data_fcm')
        
#         # convert json format 
#         data = list(map(lambda r: dict(zip(fcm_token_field_names, r)), result))
#         logger.info(msg)
#         return handle_success_with_data(msg,data)
    
#     except Exception as unexpected_error:
#         logger.exception(f"Unexpected error: {str(unexpected_error)}")
#         return server_error_response(f"Unexpected error: {str(unexpected_error)}")
 
 
 
# async def update_view_and_count_status(request, db):
#     try:
#         logger.info("The request data: %s",request)
        
#         notification_ids = request.notification_id
        
#         # check the data if present the table 
#         existing_ids = get_filtered_fields(
#             db, 
#             Notification, 
#             [Notification.notification_id], 
#             [Notification.notification_id.in_(notification_ids)]
#         )
#         logger.info("Get the notification ids: %s",existing_ids)
#         if not existing_ids:
#             logger.error("Invalid notification id.")
#             return bad_request_response("Invalid notification id.")
        
#         # Flatten list of tuples to just a list of IDs
#         existing_ids_set = {id_[config.index_zero] for id_ in existing_ids}
        
#         # Find missing IDs
#         missing_ids = set(notification_ids) - existing_ids_set
#         logger.info("Missing ids: %s",missing_ids)
#         if missing_ids:
#             logger.error(f"Invalid notification id: {sorted(missing_ids)}")
#             return bad_request_response(notification_response_message('Error','invalid_id'))

#         # flag variable using navigate operations
#         if request.flag == False:
#             logger.info("Starting the update view status flow.")
#             notification_id = request.notification_id[config.index_zero]
#             logger.info("Customer id: %s",notification_id)
#             filter_condition = (Notification.notification_id == notification_id)
#             update_data = {Notification.view_status: config.status_false}
            
#         else:
#             logger.info("Starting the update count status flow.")
            
#             notification_ids = request.notification_id
#             logger.info("Customer ids: %s",notification_ids)
#             filter_condition=Notification.notification_id.in_(notification_ids)
#             update_data={Notification.count_status: config.status_false}
         
#         # Update the data. 
#         rows_updated = update_records(
#             db=db,
#             model=Notification,
#             filter_condition=filter_condition,
#             update_data=update_data
#         )
        
#         logger.info("Update result check: %s",rows_updated)
#         if not rows_updated :
#             logger.error("A notification with this booking ID already exists.")
#             return server_error_response(notification_response_message('Error','already_exist'))

#         db.commit()
#         logger.info("Notification updated successfully.")
#         return handle_success(notification_response_message('Success','notification_update'))
    
#     except Exception as unexpected_error:
#         logger.exception(f"Unexpected error: {str(unexpected_error)}")
#         db.rollback()
#         return server_error_response(f"Unexpected error: {str(unexpected_error)}")

# def validate_venue_and_notification(db, venue_id, turf_owner_notification_id):
#     result = (
#         db.query(Venue, TurfOwnerNotification)
#         .outerjoin(TurfOwnerNotification, TurfOwnerNotification.venue_id == Venue.venue_id)
#         .filter(
#             Venue.venue_id == venue_id,
#             TurfOwnerNotification.turf_owner_notification_id == turf_owner_notification_id
#         )
#         .first()
#     )

#     if not result:
#         # Could be either or both missing
#         venue = db.query(Venue).filter(Venue.venue_id == venue_id).first()
#         notification = db.query(TurfOwnerNotification).filter(
#             TurfOwnerNotification.turf_owner_notification_id == turf_owner_notification_id
#         ).first()

#         if not venue and not notification:
#             logger.error("Both venue_id and turf_owner_notification_id not found.")
#             return False, bad_request_response("Both venue_id and turf_owner_notification_id not found.")
#         elif not venue:
#             logger.error(f"Venue with id {venue_id} not found.")
#             return False, bad_request_response(f"Venue with id {venue_id} not found.")
#         else:
#             logger.error(f"TurfOwnerNotification with id {turf_owner_notification_id} not found.")
#             return False, bad_request_response(f"TurfOwnerNotification with id {turf_owner_notification_id} not found.")

#     # venue, notification = result
#     return True , None

# from sqlalchemy import update


# def update_notification_statuses(db, turf_owner_notification_id, venue_id):
#     try:
#         # Update only one row's view_status
#         db.execute(
#             update(TurfOwnerNotification)
#             .where(TurfOwnerNotification.turf_owner_notification_id == turf_owner_notification_id)
#             .values(view_status="False")
#         )

#         # Update all rows with this venue_id's count_status
#         db.execute(
#             update(TurfOwnerNotification)
#             .where(TurfOwnerNotification.venue_id == venue_id)
#             .values(count_status="False")
#         )

#         db.commit()
#         return True
#     except Exception as e:
#         db.rollback()
#         return False



# async def update_turf_notifications(request, db):
#     try:
#         logger.info("The request data: %s",request)
        
#         turf_owner_notification_id = request.turf_owner_notification_id
#         venue_id = request.venue_id
        
        
#         status, msg = validate_venue_and_notification(db, venue_id, turf_owner_notification_id)
#         logger.info("Result: %s",status)
        
#         if not status:
#             return msg
        
        
#         update_result = update_notification_statuses(db, turf_owner_notification_id, venue_id)
#         logger.info("Update result : %s",update_result)
#         if not update_result:
#             logger.error("Update turf notification throwed error.")
#             return server_error_response("Update turf notification throwed error.")
       
#         # db.commit()
#         logger.info("Notification updated successfully.")
#         return handle_success(notification_response_message('Success','notification_update'))
    
#     except Exception as unexpected_error:
#         logger.exception(f"Unexpected error: {str(unexpected_error)}")
#         db.rollback()
#         return server_error_response(f"Unexpected error: {str(unexpected_error)}")
