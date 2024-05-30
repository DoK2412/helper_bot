from sqlmodel import SQLModel, Field
from typing import Optional


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int
    registration_date: str
    active: bool
    telegram_teg: str


class Notes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    date: str
    note: str
    creation_date: str
    sticker: str
