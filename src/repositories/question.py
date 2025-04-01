from src.models.question import Question
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.schemas.question import SQuestionCreate, SQuestionUpdate


class QuestionsRepository(BaseSQLAlchemyRepository[Question, SQuestionCreate, SQuestionUpdate]):
    _model = Question
