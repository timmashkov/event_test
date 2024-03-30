from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from .user import User


class Teacher(User):
    __tablename__ = "teacher"

    first_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    degree: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    exp: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
