from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GetFeedbackById(BaseModel):
    id: UUID


class GetFeedbackByTitle(BaseModel):
    title: str


class UpdateFeedback(GetFeedbackByTitle):
    body: str


class RegisterFeedback(UpdateFeedback):
    author_id: UUID


class FeedbackReturn(GetFeedbackById, RegisterFeedback):
    created_at: datetime
