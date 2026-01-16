from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List

class Item(BaseModel):
    model_config = ConfigDict(extra="ignore")
    product: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., gt=0)
    @field_validator("product")
    @classmethod
    def clean_product(cls, v: str) -> str:
        return v.strip()


class Invoice(BaseModel):
    model_config = ConfigDict(extra="ignore")
    order_id: str = Field(..., min_length=1)
    order_date: date
    customer_id: str = Field(..., min_length=1)
    items: List[Item] = Field(default_factory=list)
    def total_value(self) -> float:
        return float(sum(i.quantity * i.unit_price for i in self.items))
