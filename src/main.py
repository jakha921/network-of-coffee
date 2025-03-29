from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.core.config import settings


# from app.routers import router as app_router
# from users.routers import router as users_router


app = FastAPI(
    title="Cafe Network API",
    description="API for Cafe Network",
    version=settings.VERSION,
    docs_url=f"/{settings.API_PREFIX}",
    openapi_url=f"/{settings.API_PREFIX}/openapi.json",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if not settings.BACKEND_CORS_ORIGINS else settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# include routers
# app.include_router(app_router)
# app.include_router(users_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )


if __name__ == '__main__':
    import uvicorn

    # run server with command: uvicorn main:app --reload
    uvicorn.run("main:app", reload=True)
    # uvicorn.run(app, host="localhost", port=8000)