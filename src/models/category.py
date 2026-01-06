from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    main_category: str
    sub_category: str = Field(unique=True) 