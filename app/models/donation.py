from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import CharityBase


class Donation(CharityBase):
    __tablename__ = 'donation'

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)