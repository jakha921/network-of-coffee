from src.models.answer import Answer
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.schemas.answer import SAnswerCreate, SAnswerUpdate

class AnswersRepository(BaseSQLAlchemyRepository[Answer, SAnswerCreate, SAnswerUpdate]):
    _model = Answer
