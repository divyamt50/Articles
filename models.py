from datetime import datetime


from sqlalchemy import String, Text, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    email:Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    articles:Mapped[list["Article"]] = relationship(back_populates="author")

class Article(Base):
    __tablename__ = "articles"

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(255), nullable=False)
    description:Mapped[str] = mapped_column(Text)
    author_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at:Mapped[datetime] = mapped_column(default = func.now())

    author:Mapped["User"] = relationship(back_populates="articles")