from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models import Base

if TYPE_CHECKING:
    from .company import Company
    from .teacher import Teacher


class Course(Base):
    __tablename__ = "course"

    title: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, unique=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, unique=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False, unique=False)

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE")
    )
    organization: Mapped["Company"] = relationship(
        "Company",
        back_populates="courses",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )

    teachers: Mapped[list["Teacher"]] = relationship("Teacher", back_populates="course")
