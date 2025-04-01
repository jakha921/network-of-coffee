from typing import List, Optional

from pydantic import BaseModel

from src.schemas.answer import SAnswerRead


class QuestionBase(BaseModel):
    question_text: str
    sequence_number: Optional[int] = None
    is_multiple: Optional[bool] = None
    is_popup: Optional[bool] = None
    step: Optional[int] = None
    is_single: Optional[bool] = None


class SQuestionCreate(QuestionBase):
    pass


class SQuestionUpdate(QuestionBase):
    question_text: Optional[str] = None



class SQuestionRead(QuestionBase):
    id: int
    answers: List[SAnswerRead] = []  # Relationship to Answer

    class Config:
        from_attributes = True


# Example instance for testing
example_question = SQuestionRead(
    id=1,
    question_text="What is your favorite color?",
    sequence_number=1,
    is_multiple=False,
    is_popup=False,
    step=1,
    is_single=True,
    answers=[
        {
            "id": 1,
            "question_id": 1,
            "answer_text": "Red",
            "created_at": "2021-09-30T12:00:00",
        },
        {
            "id": 2,
            "question_id": 1,
            "answer_text": "Blue",
            "created_at": "2021-09-30T12:00:00",
        },
    ]
)
