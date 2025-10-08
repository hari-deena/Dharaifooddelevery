from fastapi import APIRouter
from app.routes.user import user_router
from app.routes.restaurant import restaurant_router
from app.routes.restaurant_operational import restaurant_operational_router
from app.routes.menu import menu_router






index_router = APIRouter()
index_router.include_router(user_router, prefix="/user", tags=["user"])
index_router.include_router(restaurant_router, prefix="/restaurant", tags=["restaurant"])
index_router.include_router(restaurant_operational_router, prefix="/restaurant", tags=["restaurant"])
index_router.include_router(menu_router, prefix="/restaurant", tags=["restaurant"])



