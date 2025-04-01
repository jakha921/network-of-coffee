from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.session import get_session
from src.repositories.answer import AnswersRepository
from src.schemas.answer import SAnswerRead, SAnswerCreate, SAnswerUpdate
from src.schemas.common import IGetResponseBase, IPostResponseBase

router = APIRouter()

@router.get(
    "/",
    response_description="Get all answers",
    response_model=IGetResponseBase[List[SAnswerRead]],
)
async def get_answers(
        session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[SAnswerRead]]:
    answers_repo = AnswersRepository(db=session)
    answers = await answers_repo.all()
    return IGetResponseBase[List[SAnswerRead]](data=[a.dict() for a in answers])

@router.post(
    "/",
    response_description="Create a new answer",
    response_model=IPostResponseBase[SAnswerRead],
)
async def create_answer(
        answer: SAnswerCreate,
        session: AsyncSession = Depends(get_session),
) -> IPostResponseBase[SAnswerRead]:
    answers_repo = AnswersRepository(db=session)
    new_answer = await answers_repo.create(answer)
    print('\nnew_answer:', new_answer)
    return IPostResponseBase[SAnswerRead](data=new_answer.dict())

@router.get(
    "/{id}",
    response_description="Get answer by ID",
    response_model=IGetResponseBase[SAnswerRead],
)
async def get_answer_by_id(
        id: int,
        session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[SAnswerRead]:
    answers_repo = AnswersRepository(db=session)
    answer = await answers_repo.get(id=id)
    return IGetResponseBase[SAnswerRead](data=answer.dict())

@router.patch(
    "/{id}",
    response_description="Update answer by ID",
    response_model=IPostResponseBase[SAnswerRead],
)
async def update_answer_by_id(
        id: int,
        answer: SAnswerUpdate,
        session: AsyncSession = Depends(get_session),
) -> IPostResponseBase[SAnswerRead]:
    answers_repo = AnswersRepository(db=session)
    current_answer = await answers_repo.get(id=id)
    updated_answer = await answers_repo.update(obj_current=current_answer, obj_in=answer)
    return IPostResponseBase[SAnswerRead](data=updated_answer.dict())

@router.delete(
    "/{id}",
    response_description="Delete answer by ID"
)
async def delete_answer_by_id(
        id: int,
        session: AsyncSession = Depends(get_session),
) -> None:
    answers_repo = AnswersRepository(db=session)
    try:
        await answers_repo.delete(id=id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return None
