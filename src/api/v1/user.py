from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import responses
from starlette import status

from src.db.session import get_session
from src.repositories.answer import AnswersRepository
from src.repositories.auth import create_access_token
from src.repositories.auth import create_refresh_token
from src.repositories.auth import hash_password
from src.repositories.question import QuestionsRepository
from src.repositories.user import UserRepository
from src.schemas.common import IGetResponseBase
from src.schemas.common import IPostResponseBase
from src.schemas.user import SUserCreate
from src.schemas.user import SUserRead
from src.schemas.user import SUserUpdate

router = APIRouter()


@router.get(
    "/",
    response_description="Get all users",
    response_model=IGetResponseBase[List[SUserRead]],
)
async def get_users(
    session: AsyncSession = Depends(get_session),
    email: str = None,
    uuid: str = None
) -> IGetResponseBase[List[SUserRead]]:
    user_repo = UserRepository(db=session)
    users = await user_repo.all(
        relations=[
            'analytics',
            'selected_answers',
            'payments',
            "children",
            "subscriptions"
        ],
        uuid=uuid,
        email=email
    )

    question_repo = QuestionsRepository(db=session)
    question = await question_repo.get(
        question_text="What kind of game themes might your child enjoy?"
    )

    answer_repo = AnswersRepository(db=session)
    answers = await answer_repo.all(question_id=question.id)

    response_data = []
    for user in users:
        user_dict = SUserRead.from_orm(user)
        response_data.append(user_dict)

        user_dict.subscriptions = user_dict.subscriptions[::-1]

        if user.selected_answers:
            selected_answer = next(
                (answer for answer in user.selected_answers 
                 if answer.question_id == question.id),
                None
            )
            if selected_answer:
                # Check if custom_answer is digit or not
                if selected_answer.custom_answer.isdigit():
                    user_dict.interests = [
                        answer.answer_text 
                        for answer in answers 
                        if answer.id == int(selected_answer.custom_answer)
                    ]
                else:
                    list_int = list(
                        map(
                            int,
                            selected_answer.custom_answer.replace(' ', '').split(',')
                        )
                    )
                    user_dict.selected_interests = [
                        answer.answer_text 
                        for answer in answers 
                        if answer.id in list_int
                    ]

        if user.kids_age:
            child_levels = {
                2: "Toddler",
                3: "PreK1",
                4: "PreK2",
                5: "Kindergarten",
                6: "Grade"
            }
            user_dict.child_level = child_levels.get(user.kids_age, "Toddler")

    return IGetResponseBase[List[SUserRead]](data=response_data)


@router.post(
    "/",
    response_description="Create a new user",
)
async def create_user(
        user: SUserCreate,
        session: AsyncSession = Depends(get_session),
) -> Any:
    try:
        user_repo = UserRepository(db=session)

        existing_user = await user_repo.get(email=user.email)
        if existing_user:
            return responses.JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": "error",
                    "message": "User with this email already exists"
                }
            )

        if user.password:
            user.password = hash_password(user.password)

        new_user = await user_repo.get_or_create(obj_in=user, email=user.email)

        if new_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User cannot be created"
            )

        access_token = create_access_token({"sub": str(new_user.id)})
        refresh_token = create_refresh_token({"sub": str(new_user.id)})

        return {
            "message": "User created successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "data": new_user.dict()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/{id_or_uuid}",
    response_description="Get user by id",
    response_model=IGetResponseBase[SUserRead],
)
async def get_user_by_id(
        id_or_uuid: str,
        session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[SUserRead]:
    user_repo = UserRepository(db=session)

    if id_or_uuid.isdigit():
        filter_params = {'id': int(id_or_uuid)}
    else:
        filter_params = {'uuid': id_or_uuid}

    user = await user_repo.get(
        relations=[
            'analytics',
            'selected_answers',
            'payments',
            'children',
            'subscriptions',
        ],
        **filter_params
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or has been deleted"
        )

    return IGetResponseBase[SUserRead](data=SUserRead.from_orm(user))


@router.patch(
    "/{id_or_uuid}",
    response_description="Update user by id",
    response_model=IPostResponseBase[SUserRead],
)
async def update_user_by_id(
        id_or_uuid: str,
        user: SUserUpdate,
        session: AsyncSession = Depends(get_session),
) -> IPostResponseBase[SUserRead]:
    user_repo = UserRepository(db=session)

    if id_or_uuid.isdigit():
        filter_params = {'id': int(id_or_uuid)}
    else:
        filter_params = {'uuid': id_or_uuid}

    current_user = await user_repo.get(**filter_params)

    if user.password:
        user.password = hash_password(user.password)

    updated_user = await user_repo.update(
        obj_current=current_user,
        obj_in=user
    )

    return IPostResponseBase[SUserRead](data=updated_user.dict())


@router.delete(
    "/{id_or_uuid}",
    response_description="Delete user by id"
)
async def delete_user_by_id(
        id_or_uuid: str,
        session: AsyncSession = Depends(get_session),
) -> None:
    user_repo = UserRepository(db=session)
    try:
        if id_or_uuid.isdigit():
            filter_params = {'id': int(id_or_uuid)}
        else:
            filter_params = {'uuid': id_or_uuid}
        await user_repo.delete(**filter_params)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return None
