from typing import Optional
from pydantic import BaseModel

from src.schemas.category_out import CategoryOut
from src.schemas.history_out import HistoryOut

class ProductWithLatestHistory(BaseModel):
    id: int
    name: str
    sku: str
    brand: str
    category: CategoryOut
    store: str
    url: Optional[str] = None
    history: HistoryOut