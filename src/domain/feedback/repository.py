from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.feedback.schema import (
    GetFeedbackById,
    GetFeedbackByTitle,
    UpdateFeedback,
    RegisterFeedback,
    FeedbackReturn,
)
from infrastructure.database.models import Feedback
from infrastructure.database.session import vortex


class FeedbackShowRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Feedback

    async def get_feedbacks(self) -> list[Feedback]:
        stmt = select(self.model).order_by(self.model.created_at)
        answer = await self.session.execute(stmt)
        result = list(answer.scalars().all())
        return result

    async def get_feedback_by_id(self, cmd: GetFeedbackById) -> FeedbackReturn | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_feedback_by_title(
        self, cmd: GetFeedbackByTitle
    ) -> FeedbackReturn | None:
        stmt = select(self.model).where(self.model.title == cmd.title)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result


class FeedbackDataManagerRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Feedback

    async def create_feedback(self, cmd: RegisterFeedback) -> FeedbackReturn | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.title,
                self.model.body,
                self.model.created_at,
                self.model.author_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_feedback(
        self, cmd: UpdateFeedback, model_id: GetFeedbackById
    ) -> FeedbackReturn | None:
        stmt = (
            update(self.model)
            .where(self.model.id == model_id.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.title,
                self.model.body,
                self.model.created_at,
                self.model.author_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_feedback(self, model_id: GetFeedbackById) -> FeedbackReturn | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == model_id.id)
            .returning(
                self.model.id,
                self.model.title,
                self.model.body,
                self.model.created_at,
                self.model.author_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
