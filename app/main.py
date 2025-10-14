from fastapi import FastAPI,Request
from app.routes.index import index_router
import uvicorn,logging
from starlette.middleware.cors import CORSMiddleware
from app.models.table_management import Base, engine 
from app.core.database_config import SessionLocal
import os
from mangum import Mangum
import uvicorn
from dotenv import load_dotenv
import logging
import firebase_admin
from firebase_admin import credentials
from app.core.logger_config import configure_logger

logger = configure_logger()


ENV_FILE = os.getenv('ENV_FILE', '.env.dev')
load_dotenv(ENV_FILE)

# Create the FastAPI app instance
# app = FastAPI()
app = FastAPI(
    title="Justplay Notification Services",
    description="Manage notification",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json', # This line solved my issue, in my case it was a lambda function
    root_path='/dev/',
    redoc_url=None
)

app.include_router(index_router, prefix="/dharaifood")


# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Create the Lambda handler using Mangum
handler = Mangum(app)

from .utils.response_handling import CustomAuthException
from fastapi.responses import JSONResponse
# --- ADD THIS EXCEPTION HANDLER ---
@app.exception_handler(CustomAuthException)
async def custom_auth_exception_handler(request, exc: CustomAuthException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "status_code": exc.status_code,
            "message": exc.message,   # 👈 This is YOUR field name!
        },
    )


# def init_firebase():
#     if not firebase_admin._apps:
#         cred = credentials.Certificate("app/services/serviceAccountKey.json")
#         firebase_admin.initialize_app(cred)

@app.get("/")
def get_welcome_message(request: Request):
  logger.info(f"{request.headers}")
  return {"message": "Welcome to Notification Services app!"}

# Create the database tables on startup
@app.on_event("startup")
def on_startup():
  logger.info("Creating database tables on startup")
#   init_firebase()
  Base.metadata.create_all(bind=engine)

# Close the database session on shutdown
@app.on_event("shutdown")
def shutdown():
  logger.info("Shutting down and closing database connections")
  db = SessionLocal()
  db.close()

from fastapi.exceptions import RequestValidationError
from app.utils.response_handling import bad_request_response
from app.utils import config

# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        loc = error["loc"]
        field_name = loc[-1] if isinstance(loc[-1], str) else loc[-2] if len(loc) > 1 else "body"
        error_message = error["msg"].replace("Value error, ", "")
        error_message = config.CUSTOM_ERROR_MESSAGES.get(error_message, error_message)
        combined_error = f"{field_name}: {error_message}" if field_name != "body" else error_message
    return bad_request_response(combined_error)





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv('PORT'))
