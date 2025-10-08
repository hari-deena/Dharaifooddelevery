import jwt
import datetime

# Secret key (keep it safe, not in code)
SECRET_KEY = "food_app"

# Function to generate JWT (30 days validity)
def create_jwt_token(data: dict):
    """
    Create a JWT token valid for 30 days.
    """
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# Function to decode JWT
def decode_jwt_token(token: str):
    """
    Decode JWT token and verify validity.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return (True , decoded)
    except jwt.ExpiredSignatureError:
        return (False, "Token has expired")
    except jwt.InvalidTokenError:
        return  (False, "Invalid token")

