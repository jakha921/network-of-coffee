from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class QuestionBase(SQLModel):
    question_text: str = Field(..., description="Text of the question")
    sequence_number: int = Field(..., description="Sequence number of the question", nullable=True)
    is_multiple: bool = Field(..., description="Whether the question allows multiple answers", nullable=True)
    is_popup: bool = Field(..., description="Whether the question is displayed as a popup", nullable=True)
    step: int = Field(..., description="Step number in the questionnaire process", nullable=True)
    is_single: bool = Field(..., description="Whether the question allows a single answer", nullable=True)


class Question(QuestionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relationships
    answers: List["Answer"] = Relationship(back_populates="question")
    selected_answers: List["SelectedAnswer"] = Relationship(back_populates="question")
