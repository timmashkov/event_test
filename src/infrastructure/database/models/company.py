from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models import Base


class Company(Base):
    __tablename__ = "company"

    name: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, default="Пользователь"
    )
    bio: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
