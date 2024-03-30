from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models import Base

if TYPE_CHECKING:
    from .user import User


class Role(Base):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, default="Пользователь"
    )

    user: Mapped["User"] = relationship("User", back_populates="role")
