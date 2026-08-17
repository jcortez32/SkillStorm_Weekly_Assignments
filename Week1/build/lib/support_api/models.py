from pydantic import BaseModel, Field
from typing import Literal
class RestockItem(BaseModel):
    sku: str
    warehouse: str
    quantity: int = Field(gt = 0)
    unit_cost: float = Field(gt = 0)
    category: Literal["electronics", "perishable", "apparel", "hardware"]

