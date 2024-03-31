from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models import Base

if TYPE_CHECKING:
    from .employer import Employer
    from .course import Course


class Company(Base):
    __tablename__ = "company"

    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    command: Mapped[list["Employer"]] = relationship(
        "Employer", back_populates="company"
    )

    courses: Mapped[list["Course"]] = relationship(
        "Course", back_populates="organization"
    )
