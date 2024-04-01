from uuid import UUID

from fastapi import APIRouter, Depends, status

from domain.feedback.schema import (
    GetFeedbackById,
    GetFeedbackByTitle,
    UpdateFeedback,
    RegisterFeedback,
    FeedbackReturn,
)
from infrastructure.database.models import Feedback
from service.feed_service import FeedbackShowService, FeedbackDataManagerService

feed_router = APIRouter(prefix="/feedbacks")


@feed_router.get("/all", response_model=list[FeedbackReturn])
async def show_all_feed(
    repository: FeedbackShowService = Depends(FeedbackShowService),
) -> list[Feedback]:
    return await repository.get_all_feedbacks()


@feed_router.get("/search_id/{feed_id}", response_model=FeedbackReturn)
async def show_feed_by_id(
    feed_id: UUID, repository: FeedbackShowService = Depends(FeedbackShowService)
) -> FeedbackReturn:
    return await repository.find_feedback_by_id(cmd=GetFeedbackById(id=feed_id))


@feed_router.get("/title/{title}", response_model=FeedbackReturn)
async def show_feed_by_title(
    title: str, repository: FeedbackShowService = Depends(FeedbackShowService)
) -> FeedbackReturn:
    return await repository.find_feedback_by_title(cmd=GetFeedbackByTitle(title=title))


@feed_router.post(
    "/register_teach",
    response_model=FeedbackReturn,
    status_code=status.HTTP_201_CREATED,
)
async def registration_feed(
    cmd: RegisterFeedback,
    repository: FeedbackDataManagerService = Depends(FeedbackDataManagerService),
) -> FeedbackReturn:
    return await repository.register_feedback(cmd=cmd)


@feed_router.patch("/upd/{feed_id}", response_model=FeedbackReturn)
async def upd_feed(
    feed_id: UUID,
    cmd: UpdateFeedback,
    repository: FeedbackDataManagerService = Depends(FeedbackDataManagerService),
) -> FeedbackReturn:
    return await repository.change_feedback(
        cmd=cmd, model_id=GetFeedbackById(id=feed_id)
    )


@feed_router.delete("/del/{feed_id}", response_model=FeedbackReturn)
async def del_feed(
    feed_id: UUID,
    repository: FeedbackDataManagerService = Depends(FeedbackDataManagerService),
) -> FeedbackReturn:
    return await repository.drop_feedback(model_id=GetFeedbackById(id=feed_id))
