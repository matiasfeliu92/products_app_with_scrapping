from datetime import datetime
from pydantic import BaseModel

class HistoryOut(BaseModel):
    list_price: float
    cash_price: float
    discount_pct: float
    stock: str
    installments: str
    created_at: datetime