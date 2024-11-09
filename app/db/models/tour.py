from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from app.db import Base


class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(primary_key=True)
    itinerary: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    duration: Mapped[int] = mapped_column()
    img_url: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    img_name_orig: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    img_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_reserved: Mapped[bool] = mapped_column(Boolean(), default=False)

    def __str__(self):
        return f"Тур {self.itinerary}"