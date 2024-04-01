from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.feedback.repository import (
    FeedbackShowRepository,
    FeedbackDataManagerRepository,
)
from infrastructure.cache.cache_handler import CacheService
from infrastructure.database.models import Feedback
from domain.feedback.schema import (
    GetFeedbackById,
    GetFeedbackByTitle,
    UpdateFeedback,
    RegisterFeedback,
    FeedbackReturn,
)
from infrastructure.exceptions.feed_exception import (
    FeedbackNotFound,
    FeedbackAlreadyExist,
)


class FeedbackShowService:
    def __init__(
        self,
        repository: FeedbackShowRepository = Depends(FeedbackShowRepository),
        cacher: CacheService = Depends(CacheService),
    ):
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_all_feedbacks(self) -> list[Feedback]:
        answer = await self.repository.get_feedbacks()
        await self.cacher.read_cache(self._key)
        return answer

    async def find_feedback_by_id(self, cmd: GetFeedbackById) -> FeedbackReturn:
        answer = await self.repository.get_feedback_by_id(cmd=cmd)
        if not answer:
            raise FeedbackNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def find_feedback_by_title(self, cmd: GetFeedbackByTitle) -> FeedbackReturn:
        answer = await self.repository.get_feedback_by_title(cmd=cmd)
        if not answer:
            raise FeedbackNotFound
        await self.cacher.read_cache(self._key)
        return answer


class FeedbackDataManagerService:
    def __init__(
        self,
        repository: FeedbackDataManagerRepository = Depends(
            FeedbackDataManagerRepository
        ),
        cacher: CacheService = Depends(CacheService),
    ) -> None:
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def register_feedback(self, cmd: RegisterFeedback) -> FeedbackReturn:
        try:
            answer = await self.repository.create_feedback(cmd=cmd)
            await self.cacher.create_cache(self._key, cmd.model_dump())
            return answer
        except (UniqueViolationError, IntegrityError):
            raise FeedbackAlreadyExist

    async def change_feedback(
        self, cmd: UpdateFeedback, model_id: GetFeedbackById
    ) -> FeedbackReturn:
        answer = await self.repository.update_feedback(cmd=cmd, model_id=model_id)
        if not answer:
            raise FeedbackNotFound
        await self.cacher.create_cache(self._key, cmd.model_dump())
        return answer

    async def drop_feedback(self, model_id: GetFeedbackById) -> FeedbackReturn:
        answer = await self.repository.delete_feedback(model_id=model_id)
        if not answer:
            raise FeedbackNotFound
        await self.cacher.delete_cache(self._key)
        return answer
