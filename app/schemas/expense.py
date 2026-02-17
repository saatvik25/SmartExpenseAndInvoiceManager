from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import List, Dict

class ExpenseBase(BaseModel):
    title: str
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    category: str
    date: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CategorySummary(BaseModel):
    category: str
    total: float

class ExpenseSummary(BaseModel):
    total_spent: float
    breakdown: List[CategorySummary]
