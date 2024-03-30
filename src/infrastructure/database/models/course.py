from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models import Base


class Course(Base):
    __tablename__ = "course"

    title: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, default="Пользователь"
    )
    price: Mapped[int] = mapped_column(Integer, nullable=False, unique=False)
