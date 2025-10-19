from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, DECIMAL,JSON, ForeignKey, Time, Text, TIMESTAMP, Enum, text, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.core.database_config import DATABASE_URL,sessionmaker,create_engine
from app.utils import config 
from sqlalchemy.sql import func
import enum
from sqlalchemy import Enum


Base = declarative_base()
 
UPDATE_TIMESTAMP = "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"

class Roles(Base):
    __tablename__ = 'roles' 
      
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(255), nullable=False)
    
    

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), nullable=False, unique=True)
    email = Column(String(255), nullable=True, unique=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

    roles = relationship("Roles")
    
    
class FoodType(enum.Enum):
    VEG = "VEG"
    NONVEG = "NONVEG"
    MIXED = "MIXED"  # 👈 Better than "BOTH"
    
class DeliveryType(enum.Enum):
    PARTNERED = "PARTNERED"     # Delivered by platform's delivery partners
    SELF_DELIVERY = "SELF_DELIVERY"  # Restaurant delivers on its own
    PICKUP_ONLY = "PICKUP_ONLY"      # No delivery — only pickup
    THIRD_PARTY = "THIRD_PARTY"      # Delivered via external service (e.g., Dunzo)
    SCHEDULED = "SCHEDULED"  
    
    
class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Owner user
    restaurant_name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    logo = Column(String(255))        # store image URL
    restaurant_image = Column(String(255))       # store cover image
    vat_tax = Column(Float, default=0.0)  
    cuisine = Column(JSON, nullable=False)
    food_type = Column(Enum(FoodType), default=FoodType.MIXED)
    zone = Column(String(100), nullable=False)             
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(String(20), default="ACTIVE")  
    restaurant_phone = Column(String(15), nullable=False)
    delivery_type = Column(Enum(DeliveryType), default=DeliveryType.PARTNERED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())
    

    # Relationships
    users = relationship("User")
        

class RestaurantOperationalDetails(Base):
    __tablename__ = "restaurant_operational_details"

    operational_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
    estimated_delivery_time = Column(String(50))   
    delivery_charges_per_km = Column(Float, default=0.0)  
    opening_time = Column(Time, nullable=False)  
    closing_time = Column(Time, nullable=False)  
    is_open = Column(Boolean, default=True) 

    restaurant = relationship("Restaurant")


class Cuisine(Base):
    __tablename__ = "cuisines"

    cuisine_id = Column(Integer, primary_key=True, autoincrement=True)
    cuisine_name = Column(String(100), unique=True, nullable=False)
    
    

class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("restrunt_shop.shop_id"), nullable=False)  # Changed here


    item_name = Column(String(255), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    discount_price = Column(Float)
    is_available = Column(Boolean, default=True)

    # category = Column(JSON, nullable=False) # or FK to categories table
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)

    veg_nonveg = Column(String(10), nullable=False)  # VEG / NONVEG
    preparation_time = Column(Integer)  # in minutes
    menu_images = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())
    
    restaurant = relationship("RestruntShop")
    categories = relationship("Category")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), unique=True, nullable=False)  # e.g. Starters, Main Course, Dessert, Beverages
    
    
    
# ------------------------------------------   new code  --------------------------------------------------


class RestruntShop(Base):
    __tablename__ = 'restrunt_shop'

    shop_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Owner user
    shop_name = Column(String(255), nullable=True)
    shop_address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    logtitude = Column(Float, nullable=True)  # Kept original spelling
    GST_license = Column(String(50), nullable=True)
    fssai = Column(String(14), nullable=True)
    pan = Column(String(10), nullable=True)
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(11), nullable=True)
    
    # Images as JSON (e.g., {"url": "...", "public_id": "..."} or list of URLs)
    logo = Column(JSON, nullable=True)
    banner = Column(JSON, nullable=True)
    kitchen_image = Column(JSON, nullable=True)
    
    # Special fields with defaults
    is_open = Column(Boolean, default=False, nullable=False)
    verification_status = Column(
        Enum('PENDING', 'APPROVED', 'REJECTED', name='verification_status_enum'),
        default='PENDING',
        nullable=False
    )
    
    reson_for_rejection = Column(Text, nullable=True)  # Kept original spelling

    status = Column(Enum('ACTIVE','INACTIVE', name='configurable_items_status_enum'), nullable=False,default="ACTIVE")


    # Timestamps with server defaults
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False
    )



# ---------------------------------------------- Order FLow ----------------------------------------------------



class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_status = Column(
        Enum('PENDING', 'PAID', 'FAILED', name='payment_status_enum'),
        default='PENDING',
        nullable=False
    )
    overall_status = Column(
        Enum('PLACED', 'PARTIALLY_ACCEPTED', 'ACCEPTED', 'IN_PROGRESS', 'DELIVERED', 'CANCELLED', name='order_overall_status_enum'),
        default='PLACED',
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User")
    

    
    
    
   

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("restrunt_shop.shop_id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    item_status = Column(
        Enum('PLACED', 'ACCEPTED', 'REJECTED', 'PREPARING', 'READY', 'OUT_FOR_DELIVERY', 'DELIVERED', 'CANCELLED', name='item_status_enum'),
        default='PLACED',
        nullable=False
    )

    # Relationships
    order = relationship("Order")
    shop = relationship("RestruntShop")
    menu = relationship("Menu")
    
    
    




class RestaurantOrderStatus(Base):
    __tablename__ = "restaurant_order_status"

    rest_order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("restrunt_shop.shop_id"), nullable=False)
    rest_status = Column(
        Enum('PENDING', 'ACCEPTED', 'REJECTED', 'PREPARING', 'READY_FOR_PICKUP', name='rest_status_enum'),
        default='PENDING',
        nullable=False
    )
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    order = relationship("Order")
    shop = relationship("RestruntShop")
    delivery_assignment = relationship("DeliveryAssignment")

 

class DeliveryBoy(Base):
    __tablename__ = "delivery_boy"

    delivery_boy_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False, unique=True)
    status = Column(
        Enum('AVAILABLE', 'BUSY', 'INACTIVE', name='delivery_boy_status_enum'),
        default='AVAILABLE',
        nullable=False
    )
    
    

class DeliveryAssignment(Base):
    __tablename__ = "delivery_assignment"

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    rest_order_id = Column(Integer, ForeignKey("restaurant_order_status.rest_order_id"), nullable=False)
    delivery_boy_id = Column(Integer, ForeignKey("delivery_boy.delivery_boy_id"), nullable=True)
    assign_status = Column(
        Enum('WAITING', 'ASSIGNED', 'PICKED_UP', 'DELIVERED', 'CANCELLED', name='assign_status_enum'),
        default='WAITING',
        nullable=False
    )
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    restaurant_order = relationship("RestaurantOrderStatus")
    delivery_boy = relationship("DeliveryBoy")
    
    
class OrderTracking(Base):
    __tablename__ = "order_tracking"

    track_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    entity = Column(Enum('USER', 'RESTAURANT', 'DELIVERY_BOY', 'SYSTEM', name='tracking_entity_enum'), nullable=False)
    status = Column(String(50), nullable=False)
    remarks = Column(String(500))  # or Text if very long
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    order = relationship("Order")
    
    
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    recipient_id = Column(Integer, nullable=False)
    recipient_type = Column(Enum('USER', 'RESTAURANT', 'DELIVERY_BOY'))
    title = Column(String(255))
    message = Column(Text)  # static message
    entity_type = Column(String(50))  # e.g., 'ORDER', 'DELIVERY_ASSIGNMENT'
    entity_id = Column(Integer)       # ID of the related entity
    
    
class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    
    user = relationship("User")
    menu = relationship("Menu")
    



# # Initialize database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Create all tables
Base.metadata.create_all(engine)

initial_roles = config.roles

# Check if roles already exist
existing_roles = session.query(Roles).filter(Roles.role_name.in_(initial_roles)).all()
existing_role_names = [role.role_name for role in existing_roles]

# Insert only the roles that do not already exist
roles_to_add = []
for role in initial_roles:
    if role not in existing_role_names:
        new_role = Roles(role_name=role)
        roles_to_add.append(new_role)

# Add new roles to the session and commit
if roles_to_add:
    session.add_all(roles_to_add)
    session.commit()

# Close the session 
session.close() 
