def notification_response_message(val,key):
  key_value_mapping = {
    'Success': {
        'insert_success':'Successfully insert the notification.',
        'get_success': 'Get Notification Successfully.',
        'notification_update':'Notification updated successfully.',
        'update_success': 'Successfully update the notification.',
      'no_data' : 'No data found.',
        'send_notification' : 'Successfully send notification.',
        "fcm_token_upsert_success": "Successfully inserted or updated the FCM token.",
        "success_message_fcm": "FCM tokens retrieved successfully.",
        "no_data_fcm": "No FCM tokens found for the specified customer.",
        
      },
    'Error': {
      
      'invalid_data' : 'User is not found.',
      'already_exist':'A notification with this booking ID already exists.',
      'insert_error': 'Data insertion failed.',
      'update_query_error': 'An error occurred while updating the record.',
      'send_notification_error' : "Failed to send push notification.",
      'invalid_id' : "Invalid notification id.",
      'fcm_token_missing' : "FCM token is missing in the request.",
      'firebase_connection_error' : 'Firebase connection error.',
      "user_query_error": "An error occurred while querying the user from the database.",
      "fcm_token_check_error": "An error occurred while checking if the FCM token exists.",
      "fcm_token_upsert_failed": "Failed to insert or update the FCM token in the database.",
      "error_fetching_fcm": "An error occurred while fetching FCM tokens.",
      "update_no_match" : 'No matching records found or input data is invalid.',
      }
    }
  return key_value_mapping.get(val, {}).get(key, None)
