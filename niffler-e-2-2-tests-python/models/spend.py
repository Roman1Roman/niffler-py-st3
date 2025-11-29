from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from models.category import CategoryAdd, Category


class SpendDB(SQLModel, table=True):
    __tablename__ = 'spend'
    id: str | None = Field(default=None, primary_key=True)
    amount: float
    description: str
    category_id: str = Field(foreign_key='category.id')
    spend_date: datetime
    currency: str
    username: str


class Spend(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: Category
    spendDate: datetime
    currency: str
    username: str


class SpendAdd(BaseModel):
    amount: float
    description: str
    category: CategoryAdd
    spendDate: str
    currency: str | None = Field(default="RUB")

