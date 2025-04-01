from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response

from src.api.v1 import auth, user, question, answer, contact

home_router = APIRouter()


@home_router.get("/", response_description="Homepage", include_in_schema=False)
async def home() -> Response:
    return PlainTextResponse("Web2Web2App API")


api_router = APIRouter()
api_router.include_router(auth.router, tags=["Auth"], prefix="/auth")
api_router.include_router(user.router, tags=["User"], prefix="/user")
api_router.include_router(question.router, tags=["Question"], prefix="/question")
api_router.include_router(answer.router, tags=["Answer"], prefix="/answer")
api_router.include_router(contact.router, tags=["Contact-Us"], prefix="/contact-us")
