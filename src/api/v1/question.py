from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.session import get_session
from src.repositories.question import QuestionsRepository
from src.schemas.common import IGetResponseBase, IPostResponseBase
from src.schemas.question import SQuestionRead, SQuestionCreate, SQuestionUpdate

router = APIRouter()


@router.get(
    "/",
    response_description="Get all questions",
    response_model=IGetResponseBase[List[SQuestionRead]],
)
async def get_questions(
        session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[SQuestionRead]]:
    questions_repo = QuestionsRepository(db=session)
    questions = await questions_repo.all(sort_field="id", relations=["answers"])
    # print('\nquestions:', questions)
    # print('\nquestions:', questions[0].dict())

    # Ensure answers are loaded
    # for question in questions:
    #     print(f"Question ID: {question.id}, Answers: {question.answers}")

    # Serialize using Pydantic's from_orm without extra brackets
    return IGetResponseBase[List[SQuestionRead]](data=[SQuestionRead.from_orm(q) for q in questions])


@router.post(
    "/",
    response_description="Create a new question",
    response_model=IPostResponseBase[SQuestionRead],
)
async def create_question(
        question: SQuestionCreate,
        session: AsyncSession = Depends(get_session),
) -> IPostResponseBase[SQuestionRead]:
    questions_repo = QuestionsRepository(db=session)
    new_question = await questions_repo.create(question)
    print('\nnew_question:', new_question)
    return IPostResponseBase[SQuestionRead](data=new_question.dict())


@router.get(
    "/{id}",
    response_description="Get question by ID",
    response_model=IGetResponseBase[SQuestionRead],
)
async def get_question_by_id(
        id: int,
        session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[SQuestionRead]:
    questions_repo = QuestionsRepository(db=session)
    question = await questions_repo.get(id=id)
    return IGetResponseBase[SQuestionRead](data=question.dict())


@router.patch(
    "/{id}",
    response_description="Update question by ID",
    response_model=IPostResponseBase[SQuestionRead],
)
async def update_question_by_id(
        id: int,
        question: SQuestionUpdate,
        session: AsyncSession = Depends(get_session),
) -> IPostResponseBase[SQuestionRead]:
    questions_repo = QuestionsRepository(db=session)
    current_question = await questions_repo.get(id=id)
    updated_question = await questions_repo.update(obj_current=current_question, obj_in=question)
    return IPostResponseBase[SQuestionRead](data=updated_question.dict())


@router.delete(
    "/{id}",
    response_description="Delete question by ID"
)
async def delete_question_by_id(
        id: int,
        session: AsyncSession = Depends(get_session),
) -> None:
    questions_repo = QuestionsRepository(db=session)
    try:
        await questions_repo.delete(id=id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return None
