import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
ENV_FILE = os.getenv('ENV_FILE')
load_dotenv(ENV_FILE)

# Retrieve database credentials from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

print("DB_USER: ------------> ",DB_USER)
print("DB_PASSWORD: ------------> ",DB_PASSWORD)
print("DB_HOST: ------------> ",DB_HOST)
print("DB_NAME: ------------> ",DB_NAME)




# SQLAlchemy database URL format
DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a sessionmaker to create sessions (connections) to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  
# This async generator provides a database session and ensures it is closed after use.
async def get_db():
  db = SessionLocal()
  try:
    yield db 
  finally:
    db.close()