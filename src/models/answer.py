from datetime import datetime
from typing import Optional, List

import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Relationship


class AnswerBase(SQLModel):
    question_id: int = Field(..., foreign_key="question.id", description="Reference to the question being answered")
    answer_text: str = Field(..., description="Text of the answer")


class Answer(AnswerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relationships
    question: "Question" = Relationship(back_populates="answers")
    selected_answers: List["SelectedAnswer"] = Relationship(back_populates="answer")

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
        nullable=False,
        description="Time when the record was created"
    )
