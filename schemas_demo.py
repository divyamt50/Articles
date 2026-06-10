from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    tier: str = Field(default="free", pattern="^(free|pro)$")


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    tier: str
    created_at: datetime

class ArticleCreate(BaseModel):
    title:str = Field(min_length=1, max_length=200)
    body:str = Field(min_length=1)