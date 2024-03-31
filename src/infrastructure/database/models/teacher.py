from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .course import Course


class Teacher(Base):
    __tablename__ = "teacher"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    first_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    degree: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    exp: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)

    course_id: Mapped[UUID] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"))
    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="teachers",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
