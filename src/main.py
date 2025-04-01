from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.routers import users, products, categories, orders, cart, chat, static
from src.database import engine, Base
from src.core.config import settings
from src.core.logger import setup_logging
from src.core.exceptions import BaseAPIException

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API для сети кофеен на вынос",
    version=settings.VERSION,
    docs_url=f"/{settings.API_PREFIX}/docs",
    openapi_url=f"/{settings.API_PREFIX}/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if not settings.BACKEND_CORS_ORIGINS else settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users, prefix=f"/{settings.API_PREFIX}", tags=["users"])
app.include_router(products, prefix=f"/{settings.API_PREFIX}", tags=["products"])
app.include_router(categories, prefix=f"/{settings.API_PREFIX}", tags=["categories"])
app.include_router(orders, prefix=f"/{settings.API_PREFIX}", tags=["orders"])
app.include_router(cart, prefix=f"/{settings.API_PREFIX}", tags=["cart"])
app.include_router(chat, prefix=f"/{settings.API_PREFIX}", tags=["chat"])
app.include_router(static, prefix=f"/{settings.API_PREFIX}", tags=["static"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)