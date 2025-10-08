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
    user_name = Column(String(100), nullable=False, unique=True)
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
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)

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
    
    restaurant = relationship("Restaurant")
    categories = relationship("Category")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), unique=True, nullable=False)  # e.g. Starters, Main Course, Dessert, Beverages


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
