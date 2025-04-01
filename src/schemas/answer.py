from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AnswerBase(BaseModel):
    question_id: int
    answer_text: str


class SAnswerCreate(AnswerBase):
    pass


class SAnswerUpdate(AnswerBase):
    question_id: Optional[int] = None
    answer_text: Optional[str] = None


class SAnswerRead(AnswerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Example instance for testing
example_answer = SAnswerRead(
    id=1,
    question_id=1,
    answer_text="Red",
    created_at=datetime.utcnow(),
)
