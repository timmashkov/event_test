from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models import Base

if TYPE_CHECKING:
    from .user import User


class Feedback(Base):
    __tablename__ = "feedback"

    title: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    body: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    author_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    author: Mapped["User"] = relationship(
        "User",
        back_populates="feedback",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
