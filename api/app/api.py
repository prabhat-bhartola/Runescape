from app.items.views import router as items_router
from app.ws.views import router as ws_router
from fastapi import APIRouter
from fastapi.responses import JSONResponse

api_router = APIRouter(
    default_response_class=JSONResponse,
)

api_router.include_router(items_router, prefix="/items", tags=["items"])
api_router.include_router(ws_router, prefix="/ws", tags=["ws"])
