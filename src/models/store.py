from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Store(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True) 