from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class History(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    list_price: float
    cash_price: float
    discount_pct: float
    stock: str
    installments: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    product_id: int = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="history")