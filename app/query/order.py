
from sqlalchemy import text











# def get_user_orders(
#     db, 
#     user_id: int = None, 
# ):
#     query = text("""
#         SELECT 
#     o.order_id,
#     o.total_amount,
#     o.overall_status,
#     oi.menu_id,
#     oi.quantity,
#     m.item_name,
#     m.description,
#     m.veg_nonveg,
#     m.menu_images,
#     m.discount_price,
#     m.category_id,
#     m.price,
#     rs.shop_id,
#     s.shop_name,
#     s.shop_address,
#     s.logo,
#     s.banner,
#     oi.item_status,
#     o.created_at
# FROM orders o
# JOIN order_items oi ON o.order_id = oi.order_id
# JOIN menus m ON oi.menu_id = m.menu_id
# JOIN restrunt_shop s ON oi.shop_id = s.shop_id
# JOIN restaurant_order_status rs ON rs.order_id = o.order_id AND rs.shop_id = s.shop_id
# WHERE o.user_id = :user_id
# ORDER BY o.created_at DESC;
#  """)

#     params = {
#         "user_id": user_id
#     }

#     result = db.execute(query, params).mappings().all()
#     return [dict(row) for row in result]


# def get_user_orders(db, user_id: int = None, order_id: int = None, overall_status: str = None):
#     # Base query
#     query = """
#         SELECT 
#             o.order_id,
#             o.total_amount,
#             o.overall_status,
#             oi.menu_id,
#             oi.quantity,
#             m.item_name,
#             m.description,
#             m.veg_nonveg,
#             m.menu_images,
#             m.discount_price,
#             m.category_id,
#             m.price,
#             rs.shop_id,
#             s.shop_name,
#             s.shop_address,
#             s.logo,
#             s.banner,
#             oi.item_status,
#             o.created_at
#         FROM orders o
#         JOIN order_items oi ON o.order_id = oi.order_id
#         JOIN menus m ON oi.menu_id = m.menu_id
#         JOIN restrunt_shop s ON oi.shop_id = s.shop_id
#         JOIN restaurant_order_status rs ON rs.order_id = o.order_id AND rs.shop_id = s.shop_id
#         WHERE 1=1
#     """

#     # Params dictionary
#     params = {}

#     # Add dynamic filters
#     if user_id is not None:
#         query += " AND o.user_id = :user_id"
#         params["user_id"] = user_id

#     if order_id is not None:
#         query += " AND o.order_id = :order_id"
#         params["order_id"] = order_id

#     if overall_status is not None:
#         query += " AND o.overall_status = :overall_status"
#         params["overall_status"] = overall_status

#     # Order by latest
#     query += " ORDER BY o.created_at DESC"

#     # Execute query
#     result = db.execute(text(query), params).mappings().all()

#     # Convert to list of dicts
#     return [dict(row) for row in result]


def get_user_orders(db, user_id: int = None, order_id: int = None, overall_status: str = None):
    # Base query with address join
    query = """
        SELECT 
            o.order_id,
            o.total_amount,
            o.overall_status,
            o.payment_status,
            o.created_at,
            o.updated_at,
            -- Order items
            oi.menu_id,
            oi.quantity,
            m.item_name,
            m.description,
            m.veg_nonveg,
            m.menu_images,
            m.discount_price,
            m.category_id,
            m.price,
            rs.shop_id,
            s.shop_name,
            s.shop_address,
            s.logo,
            s.banner,
            oi.item_status,
            -- Address fields
            ua.address_id,
            ua.delivery_details AS address_delivery_details,
            ua.address_details,
            ua.receiver_name,
            ua.receiver_phone,
            ua.address_save_as,
            ua.is_active AS address_is_active
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN menus m ON oi.menu_id = m.menu_id
        JOIN restrunt_shop s ON oi.shop_id = s.shop_id
        JOIN restaurant_order_status rs ON rs.order_id = o.order_id AND rs.shop_id = s.shop_id
        LEFT JOIN user_addresses ua ON ua.address_id = o.address_id
        WHERE 1=1
    """

    params = {}

    # Add filters dynamically
    if user_id is not None:
        query += " AND o.user_id = :user_id"
        params["user_id"] = user_id

    if order_id is not None:
        query += " AND o.order_id = :order_id"
        params["order_id"] = order_id

    if overall_status is not None:
        query += " AND o.overall_status = :overall_status"
        params["overall_status"] = overall_status

    # Order by latest
    query += " ORDER BY o.created_at DESC"

    # Execute query
    result = db.execute(text(query), params).mappings().all()

    # Convert to list of dicts
    return [dict(row) for row in result]


from sqlalchemy import text
from collections import defaultdict
import json

def get_restaurant_order_grouped(
    db, 
    shop_id: int = None, 
    rest_status: str = None,
):
    query = text("""
        SELECT 
            rs.rest_order_id,
            rs.order_id,
            rs.rest_status,
            oi.menu_id,
            m.item_name,
            m.price,
            oi.quantity,
            o.user_id,
            u.user_name AS customer_name,
            s.shop_name,
            o.created_at
        FROM restaurant_order_status rs
        JOIN order_items oi 
            ON oi.order_id = rs.order_id AND oi.shop_id = rs.shop_id
        JOIN menus m 
            ON m.menu_id = oi.menu_id
        JOIN orders o 
            ON o.order_id = rs.order_id
        JOIN users u 
            ON u.user_id = o.user_id
        JOIN restrunt_shop s 
            ON s.shop_id = rs.shop_id
        WHERE rs.shop_id = :restaurant_id
          AND (:rest_status IS NULL OR rs.rest_status = :rest_status)
        ORDER BY o.created_at DESC
    """)

    params = {
        "restaurant_id": shop_id,
        "rest_status": rest_status 
    }

    result = db.execute(query, params).mappings().all()
    raw_rows = [dict(row) for row in result]

    # Group by rest_order_id (each restaurant-order combo is unique)
    grouped = defaultdict(list)
    order_metadata = {}

    for row in raw_rows:
        key = row['rest_order_id']
        grouped[key].append(row)
        
        # Store metadata once per rest_order_id
        if key not in order_metadata:
            order_metadata[key] = {
                "rest_order_id": row["rest_order_id"],
                "order_id": row["order_id"],
                "customer_name": row["customer_name"],
                "shop_name": row["shop_name"],
                "status": row["rest_status"],
                "created_at": row["created_at"]
            }

    # Build final structure
    final_orders = []
    for rest_order_id, items in grouped.items():
        meta = order_metadata[rest_order_id]
        order_dict = {
            "customer_name": meta["customer_name"],
            "shop_name": meta["shop_name"],
            "rest_order_id": meta["rest_order_id"],
            "order_id": meta["order_id"],
            "status": meta["status"],
            "created_at": meta["created_at"].isoformat() if hasattr(meta["created_at"], 'isoformat') else str(meta["created_at"]),
            "items": [
                {
                    "item_name": item["item_name"],
                    "quantity": item["quantity"],
                    "price": float(item["price"]) if item["price"] is not None else None
                }
                for item in items
            ]
        }
        final_orders.append(order_dict)

    return final_orders