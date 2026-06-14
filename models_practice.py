from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Text, DateTime, func, ForeignKey
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    tier:Mapped[str] = mapped_column(String, default="Free")
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    #article:Mapped[list["Article"]] = relationship(back_populates="author")