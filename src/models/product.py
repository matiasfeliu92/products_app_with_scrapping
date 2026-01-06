from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(unique=True, index=True)
    name: str = Field(unique=True) 
    brand_id: int = Field(default=None, foreign_key="brand.id")
    category_id: int = Field(default=None, foreign_key="category.id")
    store: int = Field(default=None, foreign_key="store.id")
    history: List["History"] = Relationship(back_populates="product")
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)