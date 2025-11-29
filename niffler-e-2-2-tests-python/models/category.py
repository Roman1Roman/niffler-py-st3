from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from faker import Faker

faker = Faker()

class Category(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool


class CategoryAdd(BaseModel):
    name: str = Field(default=faker.text(max_nb_chars=7))
    username: str | None = None
    archived: bool | None = None