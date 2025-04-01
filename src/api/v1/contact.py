from fastapi import Form
from fastapi import File
from fastapi import APIRouter
from fastapi import UploadFile

from src.repositories.contact import send_email

router = APIRouter()


@router.post("/")
async def send_email_route(
    body: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(None)
):
    file_content = await file.read() if file else None
    filename = file.filename if file else None

    send_email(
        body=f"From: {email}\n\n{body}",
        attachment=file_content,
        email=email,
        filename=filename
    )

    return {"message": "Email sent successfully!"}
