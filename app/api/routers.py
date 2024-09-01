from fastapi import APIRouter
from app.api.user import routes as user_routes
from app.api.receipt import routes as receipt_routes

api_router = APIRouter()

api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
api_router.include_router(receipt_routes.router, prefix="/receipts", tags=["receipts"])
