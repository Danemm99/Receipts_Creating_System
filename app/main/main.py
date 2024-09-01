from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.routers import api_router
from app.main.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )

app.include_router(api_router, prefix=settings.API_STR)
