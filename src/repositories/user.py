import logging
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from src.models.user import User
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository, ModelType
from src.schemas.user import SUserCreate, SUserUpdate

logger = logging.getLogger(__name__)


class UserRepository(BaseSQLAlchemyRepository[User, SUserCreate, SUserUpdate]):
    _model = User

    async def delete(self, **kwargs: Any) -> bool:
        obj = await self.get(**kwargs)

        if obj:
            if obj.deleted_at:
                raise Exception(f"{self._model.__tablename__.capitalize()} not found")
        else:
            raise Exception(f"{self._model.__tablename__.capitalize()} not found")

        obj.deleted_at = datetime.utcnow()

        self.db.add(obj)
        try:
            await self.db.commit()
            await self.db.refresh(obj)
            return True

        except Exception as exc:
            await self.db.rollback()
            print(exc)
            return False

    async def all(
            self,
            skip: int = 0,
            limit: int = 100,
            sort_field: Optional[str] = None,
            sort_order: Optional[str] = None,
            relations: Optional[List[str]] = None,
            **kwargs: Any
    ) -> List[ModelType]:
        columns = self._model.__table__.columns

        if not sort_field:
            sort_field = "created_at"

        if not sort_order:
            sort_order = "desc"

        order_by = getattr(columns[sort_field], sort_order)()

        query = select(self._model).order_by(order_by).offset(skip).limit(limit)

        # add filter to deleted_at
        query = query.filter(self._model.deleted_at.is_(None))

        if kwargs:
            query = query.filter_by(**{k: v for k, v in kwargs.items() if v is not None})

        if relations:
            for relation in relations:
                query = query.options(selectinload(getattr(self._model, relation)))

        response = await self.db.execute(query)
        return response.scalars().all()

    async def get(
        self,
        relations: Optional[List[str]] = None,
        **kwargs: Any
    ) -> Optional[ModelType]:
        query = select(self._model).filter_by(**kwargs)
        query = query.filter(self._model.deleted_at.is_(None))

        if relations:
            for relation in relations:
                if hasattr(self._model, relation):
                    query = query.options(selectinload(getattr(self._model, relation))) # noqa

        response = await self.db.execute(query)
        scalar: Optional[ModelType] = response.scalar_one_or_none()

        return scalar
