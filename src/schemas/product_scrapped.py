from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional

class ProductScraped(BaseModel):
    name: str
    sku: str
    brand: str
    main_category: str
    sub_category: str
    list_price: float
    cash_price: str
    discount_applicated: str
    installments: dict
    stock: str
    warranty: Optional[str] = None
    store: str
    url: Optional[str] = None
    captured_at: datetime = Field(default_factory=datetime.utcnow)