from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import CharityBase


class CharityProject(CharityBase):
    __tablename__ = 'charity_project'

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f'Проект {self.name} '
            f'на сумму {self.full_amount}'
        )