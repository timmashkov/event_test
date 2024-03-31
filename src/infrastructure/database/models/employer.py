from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .company import Company


class Employer(Base):
    __tablename__ = "employer"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    first_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    position: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    exp: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    bio: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE")
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="command",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
