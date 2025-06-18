from app.items.views import router as items_router
from fastapi import APIRouter
from fastapi.responses import JSONResponse

api_router = APIRouter(
    default_response_class=JSONResponse,
)

api_router.include_router(items_router, prefix="/items", tags=["items"])
