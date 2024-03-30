from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, func, Text, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models import Base

if TYPE_CHECKING:
    from .role import Role


class User(Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    token: Mapped[str] = mapped_column(
        Text, unique=False, nullable=True, server_default="", default=""
    )
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship("Role", back_populates="user")
