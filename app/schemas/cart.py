from pydantic import BaseModel

class CartRequest(BaseModel):
    menu_id: int