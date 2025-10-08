from fastapi.responses import JSONResponse
from typing import Any

from fastapi import HTTPException

class CustomAuthException(HTTPException):
    def __init__(self, message: str, status_code: int = 401):
        super().__init__(status_code=status_code, detail=message)
        # We store your custom message under `.message` for later use
        self.message = message

# Returns a 200 OK JSON response with a success status, message, and data.
def handle_success_with_data(success: str, data: Any):
    return JSONResponse(
        status_code=200,
        content={"status": True, "status_code": 200, "message": success, "data": data}
    )
    
def handle_unauthorized_error(error: str = "Unauthorized access"):
    return JSONResponse(
        status_code=401,
        content={
            "status": False,
            "status_code": 401,
            "message": error,
        }
    )
    
# Returns a 200 OK JSON response with a success status and message.
def handle_success(success: str):
    return JSONResponse(
        status_code=200,
        content={"status": True, "status_code": 200, "message": success}
    )
        
# Returns a 500 Internal Server Error JSON response with a failure status and message.
def server_error_response(message):
    return JSONResponse(
        status_code=500,
        content={"status": False, "status_code": 500, "message": message}
    )

# Returns a 200 OK JSON response with a False status to indicate logical failure with a message.
def handle_success_status_false(message):
    return JSONResponse(
        status_code=200,
        content={"status": False, "status_code": 200, "message": message}
    )

# Returns a 200 OK JSON response with a False status, message, and additional data.
def handle_success_status_false_with_data(message,data):
    return JSONResponse(
        status_code=200,
        content={"status": False, "status_code": 200, "message": message,"data": data}
    )

# Returns a 400 Bad Request JSON response with a failure status and message.
def bad_request_response(error):
    return JSONResponse(
        status_code=400,
        content={"status": False, "status_code": 400, "message": error}
    )

# Returns a 400 Bad Request JSON response with a failure status, message, and data.
def bad_request_response_with_data(error: str, data: Any):
    return JSONResponse(
        status_code=400,
        content={"status": False, "status_code": 400, "message": error,"data": data}
    )

