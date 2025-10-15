from ..utils.response_handling import server_error_response, bad_request_response, handle_success_with_data,handle_success
from datetime import datetime
from app.utils import config
# from app.query.notification import get_notifications_by_customer,get_notifications_by_turf, fcm_token_field_names
# from app.query.queries import get_filtered_fields, get_first_record, insert_record, update_records
# from app.utils.email_templates import generate_booking_confirmation, generate_booking_cancellation, generate_turf_inactive_cancellation, generate_booking_completed, generate_turf_booking_confirmation_nad_cancelation
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.table_management import Order, OrderItem, RestaurantOrderStatus, Menu
from app.core.logger_config import configure_logger
from app.utils import config
import asyncio
from app.utils import config
from ..utils.common import create_jwt_token
from sqlalchemy import update
from sqlalchemy.future import select
from app.query.order import get_user_orders, get_restaurant_order_grouped
from uuid import uuid4
logger = configure_logger('justplay')


def generate_filename(file):
    """Generate a unique filename for uploaded files."""
    return f"{uuid4()}_{file.filename}"

async def add_order(request, db):
    try:
        logger.info("Order Data: %s", request)
        
        logger.info("user_id: -------------> %s",request.user_id)

        # Step 1: Create the main Order
        new_order = Order(
            user_id=request.user_id,
            total_amount=request.total_amount
        )
        db.add(new_order)
        db.flush()  # Get order_id without committing yet
        order_id = new_order.order_id
        logger.info(f"Created order with ID: {order_id}")

        # Step 2: Process order items and collect unique shops
        items = request.items
        menu_ids = [item.menu_id for item in items]
        unique_shop_ids = set(item.shop_id for item in items)

        # Fetch menu prices in bulk
        result = db.execute(select(Menu).where(Menu.menu_id.in_(menu_ids)))
        menus = result.scalars().all()
        menu_price_map = {menu.menu_id: menu.price for menu in menus}

        # Validate all menu items exist
        if len(menu_price_map) != len(menu_ids):
            missing = set(menu_ids) - set(menu_price_map.keys())
            return bad_request_response(f"Menu items not found: {missing}")

        # Create OrderItem objects
        order_items = []
        for item in items:
            price = menu_price_map[item.menu_id]
            order_item = OrderItem(
                order_id=order_id,
                shop_id=item.shop_id,
                menu_id=item.menu_id,
                quantity=item.quantity,
                price=price,
                item_status="PLACED"
            )
            order_items.append(order_item)

        db.add_all(order_items)

        # Step 3: Insert RestaurantOrderStatus — one per unique shop
        restaurant_statuses = []
        for shop_id in unique_shop_ids:
            status_entry = RestaurantOrderStatus(
                order_id=order_id,
                shop_id=shop_id,
                rest_status="PENDING"  # Default as per your model
            )
            restaurant_statuses.append(status_entry)

        db.add_all(restaurant_statuses)

        # Commit everything atomically
        db.commit()

        data = {"order_id": order_id}
        logger.info("Order, items, and restaurant statuses added successfully")
        return handle_success_with_data("Order placed successfully", data)

    except Exception as e:
        # await db.rollback()
        logger.exception("Database error while adding order: %s", str(e))
        return server_error_response("Internal server error.")
      
      
import json
from collections import defaultdict
from datetime import datetime

def group_orders_by_order_id(raw_results):
    """
    Groups raw SQL result rows by order_id and structures them into nested dictionaries.
    
    Args:
        raw_results: List of dicts from db.execute(...).mappings().all()
    
    Returns:
        List of structured orders with restaurant info and item lists.
    """
    grouped = defaultdict(list)
    
    # Group rows by order_id
    for row in raw_results:
        grouped[row['order_id']].append(row)
    
    final_orders = []
    
    for order_id, rows in grouped.items():
        # Take first row to extract common order & restaurant info
        first_row = rows[0]
        
        # Safely parse JSON-like strings (handle both '"img.png"' and '["img.png"]')
        def safe_json_loads(val):
            if not val:
                return []
            try:
                parsed = json.loads(val)
                if isinstance(parsed, str):
                    return [parsed]
                elif isinstance(parsed, list):
                    return parsed
                else:
                    return [str(parsed)]
            except (json.JSONDecodeError, TypeError):
                return [str(val)] if val else []

        restaurant_info = {
            "shop_id": first_row["shop_id"],
            "shop_name": first_row["shop_name"],
            "shop_address": first_row["shop_address"],
            "logo": safe_json_loads(first_row["logo"]),
            "banner": safe_json_loads(first_row["banner"]),
        }

        order_info = {
            "order_id": order_id,
            "total_amount": float(first_row["total_amount"]),
            "overall_status": first_row["overall_status"],
            "created_at": first_row["created_at"].isoformat() if isinstance(first_row["created_at"], datetime) else first_row["created_at"],
            "restaurant": restaurant_info,
            "items": []
        }

        # Add all items for this order
        for row in rows:
            item = {
                "menu_id": row["menu_id"],
                "item_name": row["item_name"],
                "description": row["description"],
                "veg_nonveg": row["veg_nonveg"],
                "price": float(row["price"]),
                "discount_price": float(row["discount_price"]) if row["discount_price"] is not None else None,
                "quantity": row["quantity"],
                "item_status": row["item_status"],
                "category_id": row["category_id"],
                "menu_images": safe_json_loads(row["menu_images"])
            }
            order_info["items"].append(item)
        
        final_orders.append(order_info)
    
    # Sort by created_at descending (optional, since original query already orders)
    final_orders.sort(key=lambda x: x["created_at"], reverse=True)
    
    return final_orders


async def get_user_order(user_id, db):
    try:
        logger.info("User id : ----------------------> %s",user_id)
        
        data = get_user_orders(db, user_id)
        # Assuming `result` is your list of dicts from the query
        structured_orders = group_orders_by_order_id(data)
        logger.info("Get user order successfully")
        return handle_success_with_data("Get user order successfully", structured_orders)

    except Exception as e:
        # await db.rollback()
        logger.exception("Database error while adding order: %s", str(e))
        return server_error_response("Internal server error.")

async def get_shop_orders(shop_id, rest_status, db):
    try:
        
        data = get_restaurant_order_grouped(db, shop_id, rest_status)
        print("Data: ------> ",data)
        
        # structured_orders = group_orders_by_order_id(data)
        logger.info("Get user order successfully")
        return handle_success_with_data("Get user order successfully", data)

    except Exception as e:
        # await db.rollback()
        logger.exception("Database error while adding order: %s", str(e))
        return server_error_response("Internal server error.")
 




