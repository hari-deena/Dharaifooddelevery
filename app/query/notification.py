# from sqlalchemy import text
# from ..core.logger_config import configure_logger
# logger = configure_logger('justplay')


# # This function retrieves a list of notifications for a given customer, including related booking
# # and cancellation details, ordered by the most recent notification.
# def get_notifications_by_customer(customer_id, db):
#     query = text("""
#         SELECT 
#             n.notification_id,
#             n.customer_id,
#             n.booking_id,
#             n.booking_source,
#             n.view_status,
#             n.count_status,
#             DATE_FORMAT(n.created_at, '%Y-%m-%d %H:%i:%s') AS created_time,
#             DATE_FORMAT(n.updated_at, '%Y-%m-%d %H:%i:%s') AS updated_time,
#             b.start_time,
#             b.end_time,
#             b.total_amount,
#             pd.cancellation_amount
#         FROM 
#             notifications n
#         JOIN 
#             bookings b ON n.booking_id = b.booking_id
#         LEFT JOIN (
#             SELECT booking_id, MAX(cancellation_amount) AS cancellation_amount
#             FROM payment_details
#             GROUP BY booking_id
#         ) pd ON b.booking_id = pd.booking_id
#         WHERE 
#             n.customer_id = :customer_id
#         ORDER BY 
#             n.notification_id DESC;
#     """)

#     result = db.execute(query, {"customer_id": customer_id})
#     rows = result.fetchall()
#     columns = result.keys()
    
#     # Convert each row to a dictionary
#     return [dict(zip(columns, row)) for row in rows]
    
# def get_notifications_by_turf(venue_id, db):
#     query = text("""
#         SELECT 
#             ton.turf_owner_notification_id,
#             ton.customer_id,
#             u.first_name,
#             u.last_name,
#             u.email,
#             u.mobile_number,
#             u.status AS user_status,
#             u.profile_url,
#             ton.venue_id,
#             ton.turf_id,
#             t.turf_name,
#             ton.booking_id,
#             ton.booking_source,
#             ton.view_status,
#             ton.count_status,
#             DATE_FORMAT(ton.created_at, '%Y-%m-%d %H:%i:%s') AS created_time,
#             DATE_FORMAT(ton.updated_at, '%Y-%m-%d %H:%i:%s') AS updated_time,
#             b.start_time,
#             b.end_time,
#             b.total_amount,
#             pd.cancellation_amount
#         FROM 
#             turf_owner_notifications ton
#         JOIN 
#             user u ON ton.customer_id = u.user_id
#         JOIN 
#             turfs t ON ton.turf_id = t.turf_id
#         LEFT JOIN 
#             bookings b ON ton.booking_id = b.booking_id
#         LEFT JOIN (
#             SELECT 
#                 booking_id, MAX(cancellation_amount) AS cancellation_amount
#             FROM 
#                 payment_details
#             GROUP BY 
#                 booking_id
#         ) pd ON b.booking_id = pd.booking_id
#         WHERE 
#             ton.venue_id = :venue_id
#         ORDER BY 
#             ton.turf_owner_notification_id DESC;
#     """)

#     result = db.execute(query, {"venue_id": venue_id})
#     rows = result.fetchall()
#     columns = result.keys()
    
#     # Convert each row to a dictionary
#     return [dict(zip(columns, row)) for row in rows]
    
    
# fcm_token_field_names = ["fcm_token_id", "user_id", "fcm_token"]