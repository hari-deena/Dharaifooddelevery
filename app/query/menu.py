from sqlalchemy import text

# def get_restaurant_menu(
#     db, 
#     restaurant_id: int = None, 
#     item_name: str = None, 
#     category_id: int = None, 
#     veg_nonveg: str = None
# ):
#     query = text("""
#         SELECT 
#             r.restaurant_id,
#             r.restaurant_name,
#             r.address,
#             r.logo,
#             r.restaurant_image,
#             r.vat_tax,
#             r.cuisine,
#             r.food_type,
#             r.zone,
#             r.latitude,
#             r.longitude,
#             r.status,
#             r.restaurant_phone,
#             r.delivery_type,
#             ro.is_open,
#             m.menu_id,
#             m.item_name,
#             m.description,
#             m.price,
#             m.discount_price,
#             m.is_available,
#             m.veg_nonveg,
#             m.preparation_time,
#             m.menu_images,
#             c.category_name,
#             cu.cuisine_name
#         FROM restaurants r
#         JOIN restaurant_operational_details ro 
#             ON r.restaurant_id = ro.restaurant_id
#         JOIN menus m 
#             ON r.restaurant_id = m.restaurant_id
#         JOIN categories c 
#             ON m.category_id = c.category_id
#         LEFT JOIN cuisines cu 
#             ON JSON_CONTAINS(r.cuisine, CAST(cu.cuisine_id AS JSON), '$')
#         WHERE r.status = 'ACTIVE'
#           AND ro.is_open = TRUE
#           AND m.is_available = TRUE
#           AND (:restaurant_id IS NULL OR r.restaurant_id = :restaurant_id)
#           AND (:item_name IS NULL OR m.item_name LIKE CONCAT('%', :item_name, '%'))
#           AND (:category_id IS NULL OR m.category_id = :category_id)
#           AND (:veg_nonveg IS NULL OR m.veg_nonveg = :veg_nonveg)
#     """)

#     params = {
#         "restaurant_id": restaurant_id,
#         "item_name": item_name,
#         "category_id": category_id,
#         "veg_nonveg": veg_nonveg,
#     }

#     result = db.execute(query, params).mappings().all()
#     return [dict(row) for row in result]

from ..models.table_management import Cuisine
import json

# def get_restaurant_menu(
#     db, 
#     restaurant_id: int = None, 
#     item_name: str = None, 
#     category_id: int = None, 
#     veg_nonveg: str = None
# ):
#     query = text("""
#         SELECT 
#             r.restaurant_id,
#             r.restaurant_name,
#             r.address,
#             r.logo,
#             r.restaurant_image,
#             r.vat_tax,
#             r.cuisine,
#             r.food_type,
#             r.zone,
#             r.latitude,
#             r.longitude,
#             r.status,
#             r.restaurant_phone,
#             r.delivery_type,
#             ro.is_open,
#             m.menu_id,
#             m.item_name,
#             m.description,
#             m.price,
#             m.discount_price,
#             m.is_available,
#             m.veg_nonveg,
#             m.preparation_time,
#             m.menu_images,
#             c.category_name
#         FROM restaurants r
#         JOIN restaurant_operational_details ro 
#             ON r.restaurant_id = ro.restaurant_id
#         JOIN menus m 
#             ON r.restaurant_id = m.restaurant_id
#         JOIN categories c 
#             ON m.category_id = c.category_id
#         WHERE r.status = 'ACTIVE'
#           AND ro.is_open = TRUE
#           AND m.is_available = TRUE
#           AND (:restaurant_id IS NULL OR r.restaurant_id = :restaurant_id)
#           AND (:item_name IS NULL OR m.item_name LIKE CONCAT('%', :item_name, '%'))
#           AND (:category_id IS NULL OR m.category_id = :category_id)
#           AND (:veg_nonveg IS NULL OR m.veg_nonveg = :veg_nonveg)
#     """)

#     params = {
#         "restaurant_id": restaurant_id,
#         "item_name": item_name,
#         "category_id": category_id,
#         "veg_nonveg": veg_nonveg,
#     }

#     result = db.execute(query, params).mappings().all()
#     rows = [dict(row) for row in result]

#     # 🔹 Fix: Convert JSON string into Python list before using in filter
#     for row in rows:
#         cuisine_ids = []
#         if row.get("cuisine"):
#             try:
#                 # Example: row["cuisine"] == '"[1,2,3]"' → [1,2,3]
#                 cuisine_ids = json.loads(row["cuisine"])
#                 if isinstance(cuisine_ids, str):  
#                     cuisine_ids = json.loads(cuisine_ids)  # handle double-encoded JSON
#             except Exception:
#                 cuisine_ids = []

#         if cuisine_ids:
#             cuisines = (
#                 db.query(Cuisine)
#                 .filter(Cuisine.cuisine_id.in_(cuisine_ids))
#                 .all()
#             )
#             row["cuisine"] = [
#                 {"cuisine_id": c.cuisine_id, "cuisine_name": c.cuisine_name}
#                 for c in cuisines
#             ]
#         else:
#             row["cuisine"] = []

#     return rows



def get_restaurant_menu(
    db, 
    restaurant_id: int = None, 
    restaurant_name : str = None,
    item_name: str = None, 
    category_id: int = None, 
    veg_nonveg: str = None
    
):
    query = text("""
        SELECT 
            rs.shop_id AS restaurant_id,
            rs.shop_name AS restaurant_name,
            rs.shop_address AS address,
            rs.logo,
            rs.kitchen_image,
            rs.banner AS restaurant_image,
            rs.latitude,
            rs.logtitude AS longitude,
            rs.status,
            NULL AS restaurant_phone,
            rs.is_open,
            m.menu_id,
            m.item_name,
            m.description,
            m.price,
            m.discount_price,
            m.is_available,
            m.veg_nonveg,
            m.preparation_time,
            m.menu_images,
            c.category_name
        FROM restrunt_shop rs
        JOIN menus m 
            ON rs.shop_id = m.shop_id
        JOIN categories c 
            ON m.category_id = c.category_id
        WHERE rs.status = 'ACTIVE'
          AND rs.is_open = TRUE
          AND m.is_available = TRUE
          AND (:restaurant_id IS NULL OR rs.shop_id = :restaurant_id)
          AND (:restaurant_name IS NULL OR rs.shop_name = :restaurant_name)
          AND (:item_name IS NULL OR m.item_name LIKE CONCAT('%', :item_name, '%'))
          AND (:category_id IS NULL OR m.category_id = :category_id)
          AND (:veg_nonveg IS NULL OR m.veg_nonveg = :veg_nonveg)
    """)

    params = {
        "restaurant_id": restaurant_id,
        "item_name": item_name,
        "category_id": category_id,
        "veg_nonveg": veg_nonveg,
        "restaurant_name" : restaurant_name
    }

    result = db.execute(query, params).mappings().all()
    return [dict(row) for row in result]
