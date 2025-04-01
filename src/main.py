from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.routers import users, products, categories, orders, cart, chat, static
from src.database import engine, Base
from src.core.config import settings

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Coffee Shop API",
    description="API для сети кофеен на вынос",
    version="1.0.0",
    docs_url=f"/{settings.API_PREFIX}",
    openapi_url=f"/{settings.API_PREFIX}/openapi.json",
)

@app.get("/")
async def root():
    return {"message": "Welcome to Coffee Shop API"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if not settings.BACKEND_CORS_ORIGINS else settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(users, prefix="/api", tags=["users"])
app.include_router(products, prefix="/api", tags=["products"])
app.include_router(categories, prefix="/api", tags=["categories"])
app.include_router(orders, prefix="/api", tags=["orders"])
app.include_router(cart, prefix="/api", tags=["cart"])
app.include_router(chat, prefix="/api", tags=["chat"])
app.include_router(static, prefix="/api", tags=["static"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)